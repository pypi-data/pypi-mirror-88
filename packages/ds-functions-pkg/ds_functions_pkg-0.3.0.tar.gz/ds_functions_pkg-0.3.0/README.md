# ds_functions_package
 package for storing useful data science functions

> pip install git+https://github.com/taylor-m/ds_functions_pkg

## my_functions_pkg.supervised_regression.

> ### model_cv_stats
>> (X, y, test_size, random_state, alphas, cv)
* OLS, RidgeCV, LassoCV, ElasticNetCV
* prints: best alpha, train R^2, test R^2, MAE, MSE, RMSE, MAPE
* returns: df of the cv stats

> ### predictions_df
>>(X_test, y_test, y_preds)
* returns predictions df and plotly express fig object
* data frame = X_test.copy() + y_true + y_preds + residuals + abs_residuals
* descending order by abs_residuals to view highest model mistakes made & index

> ### plot_sced_test 
>>(df, target, features)
* checks homoscedasticity assumption with plots

> ### top_corrs
>>(df, column, n=10)
* returns top (n) absolute correlated feature vars vs. target var

> ### plot_top_corrs
>>(df, column, n=10)
* plots the topp_corrs() using a facet grid

> ### tukey_outliers	
>>(df, var)
* prints outliers at each threshold (1-5)

> ### print_vif	
>>(feature_df)
* check multicollinearity assumption; prints VIF for each feature in feature_df

---
## my_functions_pkg.stats.

> ### get_95_ci
>>(x1, x2)
* 95% confidence interval

> ### cles_ind
>>(x1, x2)
* common language effect size

> ### calc_non_param_ci
>>(x1, x2, alpha=0.05)
* 2 median group test confidence interval

---


