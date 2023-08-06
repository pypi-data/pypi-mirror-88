import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import os

class Cosdem:

    def __init__(self, file_path_or_DataFrame):

        """
        :param file_path_or_DataFrame: This class accepts ->
               (.csv)  comma separated value files
               (.xls, .xlsx) excel files
               Pandas DataFrame
        """

        def __read_data(x):
            """

            :param x: This param gets the imported file

            if all Following steps are True
            Data is prepared for analysis

            :return: Pandas.Dataframe

            '''
            Data identification and verification list
            -----------------------------------------
           :exception:
            1. Format should be Excel, CSV or Pandas Dataframe
            2. The count of columns must have been two.
            3. All columns must be interger or float
            4. The count of rows must be greater than 30 for healthy statistic result
            5. Data must not have missing values.

            """

            if isinstance(x, pd.DataFrame):
                df = x

            elif x[-5:] == ".xlsx":
                df = pd.read_excel(x)

            elif x[-4:] in [".csv", ".txt"]:
                df = pd.read_csv(x)

            else:
                error = "Data must be Pandas DataFrame, CSV or xlsx (Excel) format"
                return error

            if df.shape[1] != 2:
                error = "Data has only two columns"
                return error

            if (df.dtypes[0] not in ["float64", "int64"]) or (df.dtypes[1] not in ["float64", "int64"]):
                error = "All columns must be interger or float"
                return error

            if df.shape[0] <= 30:
                error = "Rows count must be greater than 30 for healthy statistic result"
                return error

            if True in df.isnull().values:
                error = "In dataset must not have missing values"
                return error

            return df


        if isinstance(__read_data(file_path_or_DataFrame), pd.DataFrame):
            self.__df = __read_data(file_path_or_DataFrame)
        else:
            raise AttributeError(__read_data(file_path_or_DataFrame))

        """
        List of all test functions results
        """
        self.__df_list = [self._descriptive()
                          ,self._homogeneity_tests()
                          ,self._normalityTest()
                          ,self._differenceTests()
                          ,self._correlationTests()
                          ,self._regressionResult()]


    def head(self):
        """
        :return: first 5 rows in data
        """
        return self.__df.head()


    def _descriptive(self):
        df = self.__df
        descriptive = pd.DataFrame(index=["Count", "Mean", "Quantile-25", "Median (Q-50)"
            , "Quantile-75", "Std", "Variance", "Skewness"
            , "Kurtosis"])

        for i in df.columns:
            x = df[i]
            descriptive[i] = [x.count(), x.mean(), x.quantile(q=0.25)
                , x.median(), x.quantile(q=0.75), x.std()
                , x.var(), x.skew(), x.kurtosis()]

        return round(descriptive, 3)


    def _homogeneity_tests(self):
        df = self.__df
        homogeneityTests = pd.DataFrame({"Test Statistic": [stats.levene(df.iloc[:, 0], df.iloc[:, 1])[0]
            , stats.bartlett(df.iloc[:, 0], df.iloc[:, 1])[0]]
                                            , "P-value": [stats.levene(df.iloc[:, 0], df.iloc[:, 1])[1]
                , stats.bartlett(df.iloc[:, 0], df.iloc[:, 1])[1]]
                                         },
                                        index=["Levene", "Bartlett"])

        return round(homogeneityTests, 3)


    def _normalityTest(self):
        df = self.__df
        x = stats.shapiro(df.iloc[:, 0])
        y = stats.shapiro(df.iloc[:, 1])
        normalityTest = pd.DataFrame([
            [x[0], x[1]]
            , [y[0], y[1]]
            ]
            , columns=["Test Statistic", "P-value"]
            , index=[df.columns[0], df.columns[1]])

        return round(normalityTest, 3)


    def _differenceTests(self):
        df = self.__df
        t_test = stats.ttest_ind(df.iloc[:, 0], df.iloc[:, 1])
        mann_whitney = stats.mannwhitneyu(df.iloc[:, 0], df.iloc[:, 1])
        differenceTests = pd.DataFrame([
            [t_test[0], t_test[1]]
            , [mann_whitney[0], mann_whitney[1]]
            ]
            , columns=["Test Statistic", "P-value"]
            , index=["T-test", "Mann Whitney U"])

        return round(differenceTests, 3)


    def _correlationTests(self):
        df = self.__df
        pearson = stats.pearsonr(df.iloc[:, 0], df.iloc[:, 1])
        spearman = stats.spearmanr(df.iloc[:, 0], df.iloc[:, 1])
        kendall = stats.kendalltau(df.iloc[:, 0], df.iloc[:, 1])
        correlationTests = pd.DataFrame([
            [pearson[0], pearson[1]]
            , [spearman[0], spearman[1]]
            , [kendall[0], kendall[1]]
        ]
            , columns=["Test Statistic", "P-value"]
            , index=["Pearson", "Spearman", "Kendall"])

        return round(correlationTests, 3)


    def _regressionResult(self):

        df = self.__df
        x, y = df.iloc[:, 0].values, df.iloc[:, 1].values
        slope, intercept, r2, p_value, std_err = stats.linregress(x, y)

        adj_r2 = (1 - (1 - r2) * ((x.shape[0] - 1) / (x.shape[0] - 2)))

        regression_result = pd.DataFrame({"R Square": r2
                                             , "Adjusted R Square": adj_r2
                                             , "P-Value": p_value
                                             , "Coefficient": slope
                                             , "Bias": intercept}, index=[0])

        return round(regression_result, 3)


    def bland_altman_plot(self, confidence_interval=1.96, plotshow = True):
        x, y = self.__df.iloc[:, 0].values, self.__df.iloc[:, 1].values
        average = (x + y) / 2
        difference = x - y
        average_of_differences = np.mean(difference)
        std_of_differences = np.std(difference, axis=0)

        ba_plt = plt

        ba_plt.style.use('ggplot')
        ba_plt.scatter(average, difference)
        ba_plt.axhline(average_of_differences, color='red', linestyle=':')
        ba_plt.axhline(average_of_differences + confidence_interval * std_of_differences, color='blue', linestyle='--')
        ba_plt.axhline(average_of_differences - confidence_interval * std_of_differences, color='blue', linestyle='--')
        ba_plt.grid(True, color="#93a1a1", alpha=0.3)
        ba_plt.xlabel("Mean of Variables")
        ba_plt.ylabel("Percentage Difference Variables")
        # plt.legend(fontsize=14, loc ='center right')

        if plotshow == True:
            ba_plt.show()
        else:
            return ba_plt


    def regressionPlot(self, plotshow = True):
        df = self.__df

        x, y = df.iloc[:, 0].values, df.iloc[:, 1].values
        slope, intercept, _, _, _ = stats.linregress(x, y)
        resplt = plt
        resplt.style.use('ggplot')
        resplt.plot(x, y, "o", color="red")
        resplt.plot(x, x * slope + intercept, color="blue")
        resplt.xlabel(f"{df.columns[0]}")
        resplt.ylabel(f"{df.columns[1]}")

        if plotshow == True:
            resplt.show()
        else:
            return resplt


    def violinPlot(self, plotshow = True):
        df = self.__df

        vi_plt = plt

        fig, ax = vi_plt.subplots()

        violin_parts = ax.violinplot(
            df, widths=0.5, showmeans=True, showmedians=True,
            showextrema=True)

        # Make all the violin statistics marks red:
        for partname in ('cbars', 'cmins', 'cmaxes', 'cmeans', 'cmedians'):
            vp = violin_parts[partname]
            vp.set_edgecolor("green")
            vp.set_linewidth(1)

        # Make the violin body orange with a white border:
        for vp in violin_parts['bodies']:
            vp.set_facecolor("orange")
            vp.set_edgecolor("white")
            vp.set_linewidth(1)
            vp.set_alpha(0.5)

        xy = [[l.vertices[:, 0].mean(), l.vertices[0, 1]] for l in violin_parts['cmeans'].get_paths()]
        xy = np.array(xy)
        ax.scatter(xy[:, 0], xy[:, 1], s=121, c="white", marker="o", zorder=3, label="Mean")

        xy_medians = [[np.median(l.vertices[:, 0]), l.vertices[0, 1]] for l in violin_parts['cmedians'].get_paths()]
        xy_medians = np.array(xy_medians)
        ax.scatter(xy_medians[:, 0], xy_medians[:, 1], s=121, c="yellow", marker="o", zorder=3, label="Median")

        # make lines invisible
        violin_parts['cmeans'].set_visible(False)
        violin_parts['cmedians'].set_visible(False)

        # Labels
        labels = [df.columns[0], df.columns[1]]
        ax.get_xaxis().set_tick_params(direction='out')
        ax.xaxis.set_ticks_position('bottom')
        ax.set_xticks(np.arange(1, len(labels) + 1))
        ax.set_xticklabels(labels)
        ax.set_xlim(0.25, len(labels) + 0.75)

        # create a numpy image to use as a gradient
        ymin, ymax = ax.get_ylim()
        xmin, xmax = ax.get_xlim()
        Nx, Ny = 1, 1000
        imgArr = np.tile(np.linspace(0, 1, Ny), (Nx, 1)).T
        cmap = 'hsv'

        for violin in violin_parts['bodies']:
            path = Path(violin.get_paths()[0].vertices)
            patch = PathPatch(path, facecolor='none', edgecolor='none')
            ax.add_patch(patch)
            img = ax.imshow(imgArr, origin="lower", extent=[xmin, xmax, ymin, ymax], aspect="auto",
                            cmap=cmap,
                            clip_path=patch)

        # grid
        vi_plt.grid(color='gray', linestyle=':', linewidth=2)

        # drop frames
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # show plot
        vi_plt.legend()
        if plotshow == True:
            vi_plt.show()
        else:
            return vi_plt


    def save_all_figures(self):

        if "outputs" not in os.listdir():
            os.mkdir("outputs")

        r = self.regressionPlot(plotshow = False)
        r.savefig("outputs/regression.png")
        r.close()

        b = self.bland_altman_plot(plotshow = False)
        b.savefig("outputs/bland_altman.png")
        b.close()

        v = self.violinPlot(plotshow = False)
        v.savefig("outputs/violin.png")
        v.close()


        print("Successfully all figures saved in the outputs folder.")


    def save_all_tables(self):

        if "outputs" not in os.listdir():
            os.mkdir("outputs")

        writer = pd.ExcelWriter("outputs/tables.xlsx", engine='xlsxwriter')
        row = 1

        for dataframe in self.__df_list:
            dataframe.to_excel(writer, sheet_name="results", startrow=row, startcol=0)
            row = row + len(dataframe.index) + 3

        writer.save()

        print("Successfully all tables saved in the outputs folder.")


    def report(self):

        l = self.__df_list

        h1 = "-- Descriptive Statistics --"
        h2 = "-- Homogeneity Tests of Variances --"
        h3 = "-- Normality Test: Shapiro Wilk --"
        h4 = "-- Statistical Difference Tests --"
        h5 = "-- Correlation Tests --"
        h6 = "-- Regression Result --"

        return f"{h1}\n{l[0]}\n\n{h2}\n{l[1]}\n\n{h3}\n{l[2]}\n\n{h4}\n{l[3]}\n\n{h5}\n{l[4]}\n\n{h6}\n{l[5]}"

