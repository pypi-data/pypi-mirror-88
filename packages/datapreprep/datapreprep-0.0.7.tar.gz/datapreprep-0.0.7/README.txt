This is a Data pre processing package where you can Treat 
1) Missing Values using Traditional method - Mean , Median, Mode,Knn Method
2) Outlier Treatment using - IQR , Zscore
3) Feature Scaling using - Standard Scalar , Min Max Scalar, Robust Scalar, Max absolute scalar.

------------------Missing Value Treatment---------------------------------

Mean   -   treat_mean(dataframe)
Median  -  treat_median(dataframe)
Mode  -  treat_mode(dataframe)
KNN -    treat_knn(dataframe,int) # int specify nearest neighbour by default 1

---------Get information of a dataframe ---------------------------------

info(dataframe)

--------------------------Outlier Treatment-----------------------------------------------------

IQR ---  ot_iqr(dataframe,column_name)

Zscore-- ot_zscore(dataframe,column_name)


--------------------------------------Feature Scaling---------------------------------------

Standard Scalar ---   f_standardscalar(dataframe)

Min Max Scalar ---  f_minmax(dataframe)

Robust Scalar ----  f_robustscalar(dataframe)

Max absolute Scalar ---   f_maxabs(dataframe)



------------------Data Visualization----------------------------------------------------------------------


bar(df)
heatmap(df)
matrix(df)
dendrogram(df)
geoplot(df)


------------------------------You can also use the GUI version of our package---------------------------------------
       -----------We'll love it if give it a try-------------------

https://share.streamlit.io/mohammed-muzzammil/data_pre_processing/main/st1.py



-------------------------More Information on our Website-----------------------------------------
https://mohammed-muzzammil.github.io/dataprepreps




