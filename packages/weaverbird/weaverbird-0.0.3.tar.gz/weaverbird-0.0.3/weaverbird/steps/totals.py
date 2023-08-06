from typing import List

import pandas as pd
from pydantic import BaseModel, Field

from weaverbird.steps import AggregateStep, BaseStep
from weaverbird.steps.aggregate import Aggregation
from weaverbird.types import ColumnName, DomainRetriever, PipelineExecutor


class TotalDimension(BaseModel):
    total_column: ColumnName
    total_rows_label: str


class TotalsStep(BaseStep):
    name = Field('totals', const=True)
    total_dimensions: List[TotalDimension] = Field(alias='totalDimensions')
    aggregations: List[Aggregation] = Field(min_items=1)
    groups: List[ColumnName] = Field(min_items=0)

    class Config:
        allow_population_by_field_name = True

    def execute(
        self,
        df: pd.DataFrame,
        domain_retriever: DomainRetriever = None,
        execute_pipeline: PipelineExecutor = None,
    ) -> pd.DataFrame:

        df = df.copy(deep=False)

        total_rows = []
        for total_dimension in self.total_dimensions:
            total_rows.append(self.get_total_for_dimension(df, total_dimension))

        if len(self.groups) > 0:
            total_rows.append(self.get_total_for_group(df, self.groups))

        # rename columns in the base df, so it will match with the total in schema
        col_to_rm = set()
        for aggregation in self.aggregations:
            for col, new_col in zip(aggregation.columns, aggregation.new_columns):
                if col != new_col:
                    df[new_col] = df[col]
                    col_to_rm.add(col)
        for col in col_to_rm:
            del df[col]

        result = pd.concat([df] + total_rows)
        return result

    def get_total_for_group(self, df, group) -> pd.DataFrame:
        aggregation = AggregateStep(
            name='aggregate',
            keepOriginalGranularity=False,
            aggregations=self.aggregations,
            on=group,
        )
        df_result = aggregation.execute(df)
        for total_dimension in self.total_dimensions:
            df_result[total_dimension.total_column] = total_dimension.total_rows_label
        return df_result

    def get_total_for_dimension(self, df, total_dimension: TotalDimension) -> pd.DataFrame:
        # get all group_by columns: all total_dimensions, except the current one + groups
        # all columns that are either not aggregated, or groups, or total will be null
        group_by_columns = self.groups + [
            group_column.total_column
            for group_column in self.total_dimensions
            if group_column != total_dimension
        ]
        aggregation = AggregateStep(
            name='aggregate',
            keepOriginalGranularity=False,
            aggregations=self.aggregations,
            on=group_by_columns,
        )
        df_result = aggregation.execute(df)

        df_result[total_dimension.total_column] = total_dimension.total_rows_label
        if 'VQB_GROUP_BY' in df_result:
            del df_result['VQB_GROUP_BY']
        return df_result
