import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.impute import KNNImputer
import matplotlib as mpl
from matplotlib import gridspec
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
import seaborn as sns
import warnings
import random




def info(df):
    num_col =list(df.select_dtypes(include='float64').columns)
    print("The Percenatge of Value Missing in Given Data is : {:.3f}%".format((df.isna().sum().sum())/(df.count().sum())*100))
    print("\nThe Percenatge of Value Missing  in each column of  Given Data is :\n{}".format((df.isnull().sum()*100)/df.shape[0]))
    print('')
    print('Shape of dataframe (Rows, Columns): ',df.shape) # df.shape returns number of row,number of columns in form of tuple for the imported dataset 
    print('')
    print('Data description :\n',df.describe()) 
    total_column=dict((df.dtypes))
    total_column_set=set(total_column.keys())
    numerical_column_set=set(dict(df.median()).keys())
    categorical_column=list(total_column_set-numerical_column_set)
    print("The Categorical Data we have :",categorical_column)
    print('')
    print('Shape of dataframe (Rows, Columns): ',df.shape)
    print('')
    
    
   

def missing_values(df,types,n=1):
    if types == 'mean':
        clean_df=(df.fillna(df.mean()))
        clean_df.fillna(clean_df.select_dtypes(include='object').mode().iloc[0], inplace=True)
        return clean_df
    
    if types == 'median':
        clean_df=(df.fillna(df.median()))
        clean_df.fillna(clean_df.select_dtypes(include='object').mode().iloc[0], inplace=True)
        return clean_df
        
        
    if types == 'mode':
        clean_df=(df.fillna(df.mode().iloc[0]))
        return clean_df
        
        
    if types == 'knn':
        num_col =list(df.select_dtypes(include='float64').columns)
        knn =KNNImputer(n_neighbors =n,add_indicator =True)
        knn.fit(df[num_col])
        knn_impute =pd.DataFrame(knn.transform(df[num_col]))
        df[num_col]=knn_impute.iloc[:,:df[num_col].shape[1]]
        clean_df= df
        return clean_df
    
    if types == 'eod':
        extreme =df.mean()+df.std()*3 
        clean_df= df.fillna(extreme)
        return clean_df
    
    
    if types == 'capturenan':
        df1 = df.copy()
        df2 = df.copy()


        total_column=dict((df.dtypes))
        for i in total_column:
            df1[i]=np.where(df[i].isnull(),1,0) 
        df1=df1.add_suffix('_NaN')


        clean_df=(df2.fillna(df2.median()))
        clean_df.fillna(clean_df.select_dtypes(include='object').mode().iloc[0], inplace=True)
        total_column_mode=dict((clean_df.dtypes))
        for i in total_column_mode:
            clean_df[i].fillna(clean_df[i].mode(), inplace=True)


        frames = [clean_df, df1]
        result = pd.concat(frames, axis=1)
        clean_df2=result
        return clean_df2
    
    
    
    if types == 'randomsampleimputation':
        for col in df.columns:
            
            data = df[col]
            nulls = data.isnull() 
            samples = random.choices( data[~nulls].values , k = nulls.sum() ) 
            data[nulls] = samples

        return df
    

    
    
    

        

def outlier_treatment(df,column_name,types):
    if types == 'iqr':
        q1 = df[column_name].quantile(0.25)
        q3 = df[column_name].quantile(0.75)
        IQR = q3 - q1
        lower_limit = q1 - 1.5*IQR
        upper_limit = q3 + 1.5*IQR
        removed_outlier = df[(df[column_name] > lower_limit) & (df[column_name] < upper_limit)] 
        return removed_outlier
        
    
    
    
    
    
    
    if types == 'zscore':
    
        df['z-score'] = (df[column_name]-df[column_name].mean())/df[column_name].std() #calculating Z-score
        outliers = df[(df['z-score']<-1) | (df['z-score']>1)]   #outliers
        removed_outliers = pd.concat([df, outliers]).drop_duplicates(keep=False)   #dataframe after removal
        return removed_outliers
        
    
    
    
def feature_scaling(df,types):
    if types == 'standard_scalar':
        Xs = df.select_dtypes(include=np.number)
        mean_X = np.mean(Xs)
        std_X = np.std(Xs)
        Xstd = (Xs - np.mean(Xs))/np.std(Xs)
        return Xstd
            
    
    if types == 'minmax_scalar':
        Xm = df.select_dtypes(include=np.number)
        min_X = np.min(Xm)
        max_X = np.max(Xm)
        Xminmax = (Xm - Xm.min(axis = 0)) / (Xm.max(axis = 0) - Xm.min(axis = 0))
        return Xminmax
        
        
    if types == 'robust_scalar':
        Xr = df.select_dtypes(include=np.number)
        median_X = np.median(Xr)
        q3=Xr.quantile(0.75)-Xr.quantile(0.25)
        Xrs =(Xr - np.median(Xr))/q3
        return Xrs


    if types == 'maxabs_scalar':
        Xa = df.select_dtypes(include=np.number) 
        max_abs_X = np.max(abs(Xa)) 
        Xmaxabs = Xa /np.max(abs(Xa))
        return Xmaxabs
        
        
        
        
        
def nullity_sort(df, sort=None, axis='columns'):

    if sort is None:
        return df
    elif sort not in ['ascending', 'descending']:
        raise ValueError('The "sort" parameter must be set to "ascending" or "descending".')

    if axis not in ['rows', 'columns']:
        raise ValueError('The "axis" parameter must be set to "rows" or "columns".')

    if axis == 'columns':
        if sort == 'ascending':
            return df.iloc[np.argsort(df.count(axis='columns').values), :]
        elif sort == 'descending':
            return df.iloc[np.flipud(np.argsort(df.count(axis='columns').values)), :]
    elif axis == 'rows':
        if sort == 'ascending':
            return df.iloc[:, np.argsort(df.count(axis='rows').values)]
        elif sort == 'descending':
            return df.iloc[:, np.flipud(np.argsort(df.count(axis='rows').values))]
            
            
def nullity_filter(df, filter=None, p=0, n=0):

    if filter == 'top':
        if p:
            df = df.iloc[:, [c >= p for c in df.count(axis='rows').values / len(df)]]
        if n:
            df = df.iloc[:, np.sort(np.argsort(df.count(axis='rows').values)[-n:])]
    elif filter == 'bottom':
        if p:
            df = df.iloc[:, [c <= p for c in df.count(axis='rows').values / len(df)]]
        if n:
            df = df.iloc[:, np.sort(np.argsort(df.count(axis='rows').values)[:n])]
    return df
    
    
    
def bar(df, figsize=(24, 10), fontsize=16, labels=None, log=False, color='dimgray', inline=False,
        filter=None, n=0, p=0, sort=None, ax=None):
    
    
    df = nullity_filter(df, filter=filter, n=n, p=p)
    df = nullity_sort(df, sort=sort, axis='rows')
    nullity_counts = len(df) - df.isnull().sum()

    if ax is None:
        ax1 = plt.gca()
    else:
        ax1 = ax
        figsize = None  # for behavioral consistency with other plot types, re-use the given size

    (nullity_counts / len(df)).plot.bar(
        figsize=figsize, fontsize=fontsize, log=log, color=color, ax=ax1
    )

    axes = [ax1]

    # Start appending elements, starting with a modified bottom x axis.
    if labels or (labels is None and len(df.columns) <= 50):
        ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right', fontsize=fontsize)

        # Create the numerical ticks.
        ax2 = ax1.twinx()
        axes.append(ax2)
        if not log:
            ax1.set_ylim([0, 1])
            ax2.set_yticks(ax1.get_yticks())
            ax2.set_yticklabels([int(n*len(df)) for n in ax1.get_yticks()], fontsize=fontsize)
        else:
            # For some reason when a logarithmic plot is specified `ax1` always contains two more ticks than actually
            # appears in the plot. The fix is to ignore the first and last entries. Also note that when a log scale
            # is used, we have to make it match the `ax1` layout ourselves.
            ax2.set_yscale('log')
            ax2.set_ylim(ax1.get_ylim())
            ax2.set_yticklabels([int(n*len(df)) for n in ax1.get_yticks()], fontsize=fontsize)
    else:
        ax1.set_xticks([])

    # Create the third axis, which displays columnar totals above the rest of the plot.
    ax3 = ax1.twiny()
    axes.append(ax3)
    ax3.set_xticks(ax1.get_xticks())
    ax3.set_xlim(ax1.get_xlim())
    ax3.set_xticklabels(nullity_counts.values, fontsize=fontsize, rotation=45, ha='left')
    ax3.grid(False)

    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')

    if inline:
        warnings.warn(
            "The 'inline' argument has been deprecated, and will be removed in a future version "
            "of missingno."
        )
        plt.show()
    else:
        return ax1
        
        
        
        
        
def matrix(df,
           filter=None, n=0, p=0, sort=None,
           figsize=(25, 10), width_ratios=(15, 1), color=(0.25, 0.25, 0.25),
           fontsize=16, labels=None, sparkline=True, inline=False,
           freq=None, ax=None):
    
    df = nullity_filter(df, filter=filter, n=n, p=p)
    df = nullity_sort(df, sort=sort, axis='columns')

    height = df.shape[0]
    width = df.shape[1]

    # z is the color-mask array, g is a NxNx3 matrix. Apply the z color-mask to set the RGB of each pixel.
    z = df.notnull().values
    g = np.zeros((height, width, 3))

    g[z < 0.5] = [1, 1, 1]
    g[z > 0.5] = color

    # Set up the matplotlib grid layout. A unary subplot if no sparkline, a left-right splot if yes sparkline.
    if ax is None:
        plt.figure(figsize=figsize)
        if sparkline:
            gs = gridspec.GridSpec(1, 2, width_ratios=width_ratios)
            gs.update(wspace=0.08)
            ax1 = plt.subplot(gs[1])
        else:
            gs = gridspec.GridSpec(1, 1)
        ax0 = plt.subplot(gs[0])
    else:
        if sparkline is not False:
            warnings.warn(
                "Plotting a sparkline on an existing axis is not currently supported. "
                "To remove this warning, set sparkline=False."
            )
            sparkline = False
        ax0 = ax

    # Create the nullity plot.
    ax0.imshow(g, interpolation='none')

    # Remove extraneous default visual elements.
    ax0.set_aspect('auto')
    ax0.grid(b=False)
    ax0.xaxis.tick_top()
    ax0.xaxis.set_ticks_position('none')
    ax0.yaxis.set_ticks_position('none')
    ax0.spines['top'].set_visible(False)
    ax0.spines['right'].set_visible(False)
    ax0.spines['bottom'].set_visible(False)
    ax0.spines['left'].set_visible(False)

    # Set up and rotate the column ticks. The labels argument is set to None by default. If the user specifies it in
    # the argument, respect that specification. Otherwise display for <= 50 columns and do not display for > 50.
    if labels or (labels is None and len(df.columns) <= 50):
        ha = 'left'
        ax0.set_xticks(list(range(0, width)))
        ax0.set_xticklabels(list(df.columns), rotation=45, ha=ha, fontsize=fontsize)
    else:
        ax0.set_xticks([])

    # Adds Timestamps ticks if freq is not None, else set up the two top-bottom row ticks.
    if freq:
        ts_list = []

        if type(df.index) == pd.PeriodIndex:
            ts_array = pd.date_range(df.index.to_timestamp().date[0],
                                     df.index.to_timestamp().date[-1],
                                     freq=freq).values

            ts_ticks = pd.date_range(df.index.to_timestamp().date[0],
                                     df.index.to_timestamp().date[-1],
                                     freq=freq).map(lambda t:
                                                    t.strftime('%Y-%m-%d'))

        elif type(df.index) == pd.DatetimeIndex:
            ts_array = pd.date_range(df.index.date[0], df.index.date[-1],
                                     freq=freq).values

            ts_ticks = pd.date_range(df.index.date[0], df.index.date[-1],
                                     freq=freq).map(lambda t:
                                                    t.strftime('%Y-%m-%d'))
        else:
            raise KeyError('Dataframe index must be PeriodIndex or DatetimeIndex.')
        try:
            for value in ts_array:
                ts_list.append(df.index.get_loc(value))
        except KeyError:
            raise KeyError('Could not divide time index into desired frequency.')

        ax0.set_yticks(ts_list)
        ax0.set_yticklabels(ts_ticks, fontsize=int(fontsize / 16 * 20), rotation=0)
    else:
        ax0.set_yticks([0, df.shape[0] - 1])
        ax0.set_yticklabels([1, df.shape[0]], fontsize=int(fontsize / 16 * 20), rotation=0)

    # Create the inter-column vertical grid.
    in_between_point = [x + 0.5 for x in range(0, width - 1)]
    for in_between_point in in_between_point:
        ax0.axvline(in_between_point, linestyle='-', color='white')

    if sparkline:
        # Calculate row-wise completeness for the sparkline.
        completeness_srs = df.notnull().astype(bool).sum(axis=1)
        x_domain = list(range(0, height))
        y_range = list(reversed(completeness_srs.values))
        min_completeness = min(y_range)
        max_completeness = max(y_range)
        min_completeness_index = y_range.index(min_completeness)
        max_completeness_index = y_range.index(max_completeness)

        # Set up the sparkline, remove the border element.
        ax1.grid(b=False)
        ax1.set_aspect('auto')
        # GH 25
        if int(mpl.__version__[0]) <= 1:
            ax1.set_axis_bgcolor((1, 1, 1))
        else:
            ax1.set_facecolor((1, 1, 1))
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.spines['bottom'].set_visible(False)
        ax1.spines['left'].set_visible(False)
        ax1.set_ymargin(0)

        # Plot sparkline---plot is sideways so the x and y axis are reversed.
        ax1.plot(y_range, x_domain, color=color)

        if labels:
            # Figure out what case to display the label in: mixed, upper, lower.
            label = 'Data Completeness'
            if str(df.columns[0]).islower():
                label = label.lower()
            if str(df.columns[0]).isupper():
                label = label.upper()

            # Set up and rotate the sparkline label.
            ha = 'left'
            ax1.set_xticks([min_completeness + (max_completeness - min_completeness) / 2])
            ax1.set_xticklabels([label], rotation=45, ha=ha, fontsize=fontsize)
            ax1.xaxis.tick_top()
            ax1.set_yticks([])
        else:
            ax1.set_xticks([])
            ax1.set_yticks([])

        # Add maximum and minimum labels, circles.
        ax1.annotate(max_completeness,
                     xy=(max_completeness, max_completeness_index),
                     xytext=(max_completeness + 2, max_completeness_index),
                     fontsize=int(fontsize / 16 * 14),
                     va='center',
                     ha='left')
        ax1.annotate(min_completeness,
                     xy=(min_completeness, min_completeness_index),
                     xytext=(min_completeness - 2, min_completeness_index),
                     fontsize=int(fontsize / 16 * 14),
                     va='center',
                     ha='right')

        ax1.set_xlim([min_completeness - 2, max_completeness + 2])  # Otherwise the circles are cut off.
        ax1.plot([min_completeness], [min_completeness_index], '.', color=color, markersize=10.0)
        ax1.plot([max_completeness], [max_completeness_index], '.', color=color, markersize=10.0)

        # Remove tick mark (only works after plotting).
        ax1.xaxis.set_ticks_position('none')

    if inline:
        warnings.warn(
            "The 'inline' argument has been deprecated, and will be removed in a future version "
            "of missingno."
        )
        plt.show()
    else:
        return ax0
        
        
        
        
def heatmap(df, inline=False,
            filter=None, n=0, p=0, sort=None,
            figsize=(20, 12), fontsize=16, labels=True, 
            cmap='RdBu', vmin=-1, vmax=1, cbar=True, ax=None
            ):

    # Apply filters and sorts, set up the figure.
    df = nullity_filter(df, filter=filter, n=n, p=p)
    df = nullity_sort(df, sort=sort, axis='rows')

    if ax is None:
        plt.figure(figsize=figsize)
        ax0 = plt.gca()
    else:
        ax0 = ax

    # Remove completely filled or completely empty variables.
    df = df.iloc[:,[i for i, n in enumerate(np.var(df.isnull(), axis='rows')) if n > 0]]

    # Create and mask the correlation matrix. Construct the base heatmap.
    corr_mat = df.isnull().corr()
    mask = np.zeros_like(corr_mat)
    mask[np.triu_indices_from(mask)] = True

    if labels:
        sns.heatmap(corr_mat, mask=mask, cmap=cmap, ax=ax0, cbar=cbar,
                    annot=True, annot_kws={'size': fontsize - 2},
                    vmin=vmin, vmax=vmax)
    else:
        sns.heatmap(corr_mat, mask=mask, cmap=cmap, ax=ax0, cbar=cbar,
                    vmin=vmin, vmax=vmax)

    # Apply visual corrections and modifications.
    ax0.xaxis.tick_bottom()
    ax0.set_xticklabels(ax0.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=fontsize)
    ax0.set_yticklabels(ax0.yaxis.get_majorticklabels(), fontsize=fontsize, rotation=0)
    ax0.set_yticklabels(ax0.yaxis.get_majorticklabels(), rotation=0, fontsize=fontsize)
    ax0.xaxis.set_ticks_position('none')
    ax0.yaxis.set_ticks_position('none')
    ax0.patch.set_visible(False)

    for text in ax0.texts:
        t = float(text.get_text())
        if 0.95 <= t < 1:
            text.set_text('<1')
        elif -1 < t <= -0.95:
            text.set_text('>-1')
        elif t == 1:
            text.set_text('1')
        elif t == -1:
            text.set_text('-1')
        elif -0.05 < t < 0.05:
            text.set_text('')
        else:
            text.set_text(round(t, 1))

    if inline:
        warnings.warn(
            "The 'inline' argument has been deprecated, and will be removed in a future version "
            "of missingno."
        )
        plt.show()
    else:
        return ax0


def dendrogram(df, method='average',
               filter=None, n=0, p=0,
               orientation=None, figsize=None,
               fontsize=16, inline=False, ax=None
               ):
 
    if not figsize:
        if len(df.columns) <= 50 or orientation == 'top' or orientation == 'bottom':
            figsize = (25, 10)
        else:
            figsize = (25, (25 + len(df.columns) - 50) * 0.5)

    if ax is None:
        plt.figure(figsize=figsize)
        ax0 = plt.gca()
    else:
        ax0 = ax

    df = nullity_filter(df, filter=filter, n=n, p=p)

    # Link the hierarchical output matrix, figure out orientation, construct base dendrogram.
    x = np.transpose(df.isnull().astype(int).values)
    z = hierarchy.linkage(x, method)

    if not orientation:
        if len(df.columns) > 50:
            orientation = 'left'
        else:
            orientation = 'bottom'

    hierarchy.dendrogram(
        z,
        orientation=orientation,
        labels=df.columns.tolist(),
        distance_sort='descending',
        link_color_func=lambda c: 'black',
        leaf_font_size=fontsize,
        ax=ax0
    )

    # Remove extraneous default visual elements.
    ax0.set_aspect('auto')
    ax0.grid(b=False)
    if orientation == 'bottom':
        ax0.xaxis.tick_top()
    ax0.xaxis.set_ticks_position('none')
    ax0.yaxis.set_ticks_position('none')
    ax0.spines['top'].set_visible(False)
    ax0.spines['right'].set_visible(False)
    ax0.spines['bottom'].set_visible(False)
    ax0.spines['left'].set_visible(False)
    ax0.patch.set_visible(False)

    # Set up the categorical axis labels and draw.
    if orientation == 'bottom':
        ax0.set_xticklabels(ax0.xaxis.get_majorticklabels(), rotation=45, ha='left')
    elif orientation == 'top':
        ax0.set_xticklabels(ax0.xaxis.get_majorticklabels(), rotation=45, ha='right')
    if orientation == 'bottom' or orientation == 'top':
        ax0.tick_params(axis='y', labelsize=int(fontsize / 16 * 20))
    else:
        ax0.tick_params(axis='x', labelsize=int(fontsize / 16 * 20))

    if inline:
        warnings.warn(
            "The 'inline' argument has been deprecated, and will be removed in a future version "
            "of missingno."
        )
        plt.show()
    else:
        return ax0


def geoplot(df,
            filter=None, n=0, p=0,
            x=None, y=None, figsize=(25, 10), inline=False,
            by=None, cmap='YlGn', **kwargs):
  
    warnings.warn(
        "The 'geoplot' function has been deprecated, and will be removed in a future version "
        "of missingno. The 'geoplot' package has an example recipe for a more full-featured "
        "geospatial nullity plot: "
        "https://residentmario.github.io/geoplot/gallery/plot_san_francisco_trees.html"
    )
    try:
        import geoplot as gplt
    except ImportError:
        raise ImportError("Install geoplot <= 0.2.4 (the package) for geoplot function support")

    if gplt.__version__ >= "0.3.0":
        raise ImportError(
            "The missingno geoplot function requires geoplot package version 0.2.4 or lower." 
            "To use the geoplot function, downgrade to an older version of the geoplot package."
        )

    import geopandas as gpd
    from shapely.geometry import Point

    df = nullity_filter(df, filter=filter, n=n, p=p)

    nullity = df.notnull().sum(axis='columns') / df.shape[1]
    if x and y:
        gdf = gpd.GeoDataFrame(nullity, columns=['nullity'],
                               geometry=df.apply(lambda srs: Point(srs[x], srs[y]), axis='columns'))
    else:
        raise ValueError("The 'x' and 'y' parameters must be specified.")

    if by:
        if df[by].isnull().any():
            warnings.warn('The "{0}" column included null values. The offending records were dropped'.format(by))
            df = df.dropna(subset=[by])
            gdf = gdf.loc[df.index]

        vc = df[by].value_counts()
        if (vc < 3).any():
            warnings.warn('Grouping by "{0}" included clusters with fewer than three points, which cannot be made '
                          'polygonal. The offending records were dropped.'.format(by))
            where = df[by].isin((df[by].value_counts() > 2).where(lambda b: b).dropna().index.values)
            gdf = gdf.loc[where]
        gdf[by] = df[by]

    gplt.aggplot(gdf, figsize=figsize, hue='nullity', agg=np.average, cmap=cmap, by=by, edgecolor='None', **kwargs)
    ax = plt.gca()

    if inline:
        warnings.warn(
            "The 'inline' argument has been deprecated, and will be removed in a future version "
            "of missingno."
        )
        plt.show()
    else:
        return ax

        
        
        
