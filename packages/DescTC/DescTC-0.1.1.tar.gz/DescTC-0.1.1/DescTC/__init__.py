class DescTC():
    """
    It generates a range of information about the data provided and gives a better visualization of the data before the cleansing process has been done.
    Therefore, It helps you decide the best data cleansing method that should be used as your analysis starting point.
    """

    def __init__(self, df):
        self.df = df


    def table(self):
        """Analyses ``DataFrame`` column sets of mixed data types. The output
        will vary depending on the columns type. Refer to the notes
        below for more detail.
        Returns
        -------
        DataFrame
            Summary information and some of the descriptive statistics of the data provided.
        ``Type``: is the type of the column values of the column,
        ``Quant.Zeros``: is the quantity of the zero values of the column,
        ``Quant.NaNs``: is the quantity of the NaN values of the column,
        ``%NaNs``: is the percentage of the NaN values of the column,
        ``Quant.Uniques``: is the quantity of unique values of the column,
        ``Quant.Outliers``: is the quantity of unique values of the column,
        ``Min/Lowest``: is the minimum value of the numeric column or the lowest value of the categorical column,
        ``Mean``: is the average/mean of the values of the numeric column,
        ``Median``: is the 50th percentile of the numeric column,
        ``Mode``: is the most often value of the column,
        ``Max/Highest``: is the maximum value of the numeric column or the most common value of the categorical column.
        The z-score is the outlier finder method used. This method can only be used with
        a gaussian distribution. Disregard this outlier output if the distribution
        of the variable can not be assumed to be parametric.
        If multiple object values have the lowest/highest count,
        then the results will be arbitrarily chosen from
        among those with the lowest/highest count.
        Notes
        -----
        All empty columns of your data frame will be excluded and not generated in the output.
        The data must be converted to a pandas DataFrame with column names. Make the first row as a column headers.
        """

        import numpy as np
        import pandas as pd

        empty_cols = [col for col in self.df.columns if self.df[col].isnull().all()]
        self.df.drop(empty_cols, axis=1, inplace=True)
        np.seterr(divide='ignore', invalid='ignore')

        col_list = []
        zr_list = []
        unique_list = []
        miss_table = []
        outlier = []
        mean_list = []
        median_list = []
        mode_list = []
        max_list = []
        min_list = []
        O_col_name = []
        O_col_pos = []

        for colname in self.df:
            zeros = len(self.df) - np.count_nonzero(self.df[colname].tolist())
            zr_list.append(zeros)
            unique = self.df[colname].unique()
            unique_list.append(unique)
            mode = self.df[colname].mode()[0]
            mode_list.append(mode)
            col_list.append(colname)

            # Replacing question marks with np.nan
            self.df[colname] = self.df[colname].apply(lambda x: np.nan if str(x).find('?') > -1 else x)

        types = self.df.dtypes.tolist()
        nan = self.df.isna().sum().tolist()
        nanp = round((self.df.isna().sum() * 100 / len(self.df)), 2).tolist()

        # Creating a new dataFrame without the non-numeric columns and finding their names and positions to create a new df.
        for col in self.df.columns:
            if self.df.dtypes[col] == "O" or self.df.dtypes[col] == "bool":
                O_col_name.append(self.df[col].name)
                O_col_pos.append(self.df.columns.get_loc(self.df[col].name))
        df_new = self.df.drop(self.df.columns[O_col_pos], axis=1)

        # Creating another DataFrame (df_pad) with the Zscore without the non-numeric columns
        from scipy import stats
        from scipy.stats import zscore
        df_pad = stats.zscore(df_new)
        df_pad = pd.DataFrame(df_pad, columns=df_new.columns.tolist())

        # Creating a dataframe column with number 1 to replace object columns
        c_ones = np.ones(len(self.df))

        # Inserting the non-numeric columns on the df_pad (dataframe Zscore)
        for i in range(len(O_col_pos)):
            df_pad.insert(loc=O_col_pos[i], column=O_col_name[i], value=c_ones)

        # Finding quantity of outliers for each column
        for c in range(len(df_pad.columns)):
            out_col = []
            count = 0
            for j in df_pad.values[:, c]:
                if np.abs(j) > 3:
                    count += 1
            out_col.append(count)
            outlier.append(out_col)

        # Finding Max, Min, Average and median for each column
        for c in self.df.columns:
            if c not in O_col_name:
                max_list.append(self.df[c].max())
                min_list.append(self.df[c].min())
                mean_list.append(self.df[c].mean())
                median_list.append(self.df[c].median())

            else:
                max_list.append(self.df[c].value_counts().index[:1][0])
                min_list.append(self.df[c].value_counts().index[:len(self.df[c].unique())][-1])
                mean_list.append("NaN")
                median_list.append("NaN")

        # Final result
        for i in range(len(self.df.columns)):
            df_missing = [types[i], zr_list[i], nan[i], nanp[i], len(set(unique_list[i])), outlier[i], min_list[i],
                          mean_list[i], median_list[i], mode_list[i], max_list[i]]
            miss_table.append(df_missing)

        missing_table = pd.DataFrame(miss_table, index=col_list,
                                     columns=["Type", "Quant.Zeros", "Quant.NaNs", "%NaNs", "Quant.Uniques",
                                              "Quant.Outliers", "Min/Lowest", "Mean", "Median", "Mode", "Max/Highest"])
        return missing_table

    def chart(self):
        """
        This method condense large amounts of information into easy-to-understand formats
        that clearly and effectively communicate important points
        Returns
        -------
        The countplot for qualitative variables
        Plot a histogram and box plot for quantitative variables
        Plot the correlation between quantitative variables
        """

        import matplotlib.pyplot as plt
        import seaborn as sns

        empty_cols = [col for col in self.df.columns if self.df[col].isnull().all()]
        self.df.drop(empty_cols, axis=1, inplace=True)
        plt.rcParams.update({'figure.max_open_warning': 0})

        # Distribution Chart for each dataframe column
        for col in self.df.columns:
            print('Variable: \033[34m{}\033[m'.format(col))
            if self.df.dtypes[col] == "O" or self.df.dtypes[col] == "bool":
                if len(self.df[col].unique()) > 50:
                    print(
                        'Since the variable \033[32m{}\033[m has several distinct values, the visualization process through the chart is not a good option.'.format(
                            col))
                    print()
                    print()

                else:
                    plt.figure(figsize=(9, 4))
                    chart = sns.countplot(x=col, data=self.df, order=self.df[col].value_counts().index)
                    chart.set(title="Frequency Chart - {}".format(col))
                    plt.xticks(rotation=45, horizontalalignment='right')
                    plt.grid(color='gray', ls='-.', lw=0.08)
                plt.show()
                print()
                print()

            else:
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

                ax1.hist(self.df[col], label=col, bins='sqrt')
                ax1.set(title="Frequency Chart - {}".format(col), xlabel=col, ylabel="count")
                ax1.grid(color='gray', ls='-.', lw=0.08)
                plt.setp(ax1.get_xticklabels(), rotation=15)

                red_diamond = dict(markerfacecolor='r', marker='D')
                ax2.boxplot(self.df[col], flierprops=red_diamond)
                ax2.set(title="Box-plot - {}".format(col), xlabel=col, ylabel="values")
                ax2.grid(color='gray', ls='-.', lw=0.08)

                plt.show()
                print()
                print()

        # Correlation Plot
        if self.df.shape[1] <= 10:
            plt.figure(figsize=(5, 5))
        elif self.df.shape[1] <= 20:
            plt.figure(figsize=(8, 8))
        else:
            plt.figure(figsize=(20, 20))
        sns.heatmap(self.df.corr(), annot=True, cmap='RdBu')
        plt.title('Correlation Plot - Heatmap', fontsize=14)
        plt.xticks(rotation=15)
        plt.yticks(rotation=15)


    def printfullTable(self):
        """
        Useful to see the entire outcome independently on which environment you are executing the package.
        """
        import pandas as pd
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        print(self.table())
