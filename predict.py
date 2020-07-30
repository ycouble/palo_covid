#!/usr/bin/env python3
import datetime
import logging

import fire
import numpy as np
import pandas as pd
from sklearn import preprocessing
from xgboost import XGBRegressor

import etl.integration as ei

logger = logging.getLogger("palo_api")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

logger.addHandler(ch)

TEST_RATIO = 0.2



def xgboost_prediction(subset=None):
    # get data
    df = ei.get_aggregated()
    if subset:
        df = df[df['Country'].isin(subset.split(" "))]
    df = df[df['Source'] == 'srk']

    # ForecastId
    df['ForecastId'] = list(range(df.shape[0]))

    # Label encoder for countries
    logger.info("== Preprocessing Countries")
    le = preprocessing.LabelEncoder()
    df['CountryCode'] = le.fit_transform(df['Country'])
    # Get list of country labels
    countries = df['CountryCode'].unique()

    # convert dates to int
    logger.info("== Creating supplementary features")
    df['dayofyear'] = df['Date'].apply(lambda x: (x - datetime.datetime(2020, 1, 1)).days)
    df['sq_dayofyear'] = df['dayofyear'] ** 2
    df['exp_dayofyear'] = np.exp(df['dayofyear'])
    features = ['CountryCode', 'dayofyear', 'sq_dayofyear', 'exp_dayofyear']

    # get dates
    dates = df['Date'].unique()
    dates.sort()

    # split train/test
    limit = round(dates.size * (1 - TEST_RATIO))
    train_dates, test_dates = dates[:limit], dates[limit:]
    train = df[df['Date'].isin(train_dates)]
    test = df[df['Date'].isin(test_dates)]

    logger.info("== Splitting Training and Testing")
    logger.debug(
        f"Training dataset defined between: "
        f"{train['Date'].min().date()} and {train['Date'].max().date()}"
    )
    logger.debug(
        f"Testing dataset defined between: "
        f"{test['Date'].min().date()} and {test['Date'].max().date()}"
    )

    # duplicate train/test
    Xtrain, Xtest = train.copy(), test.copy()

    # Init output
    logger.info("== Initializing output")
    xout = pd.DataFrame({'ForecastId': [], 'PConfirmed': [], 'PDeaths': []})

    # Model Building
    logger.info("== Building model for each country")
    for country in countries:
        if Xtrain[Xtrain['CountryCode'] == country].shape[0] == 0:
            logger.warning(f"  -- no data for country code {country}")
            continue
        country_name = Xtrain[Xtrain['CountryCode'] == country]['Country'].iloc[0]
        logger.info(f"  -- {country} --> {country_name}")

        ## Train
        # filter per country
        Xtrain_country = Xtrain[Xtrain['CountryCode'] == country]
        # build x, y1, y2
        ytrain_1 = Xtrain_country.loc[:, 'Confirmed']
        ytrain_2 = Xtrain_country.loc[:, 'Deaths']
        xtrain = Xtrain_country.loc[:, features]

        ## Test
        # filter per country
        Xtest_country = Xtest[Xtest['CountryCode'] == country]
        # build x, x_id
        xtest = Xtest_country.loc[:, features]
        xtest_id = Xtest_country.loc[:, 'ForecastId']
        ytest_1 = Xtest_country.loc[:, 'Confirmed']
        ytest_2 = Xtest_country.loc[:, 'Deaths']

        # train model
        xmodel_1 = XGBRegressor(n_estimators=1000)
        xmodel_2 = XGBRegressor(n_estimators=1000)
        logger.debug("    training for confirmed cases")
        xmodel_1.fit(xtrain, ytrain_1)
        logger.debug("    training for deaths")
        xmodel_2.fit(xtrain, ytrain_2)

        if xtest.shape[0] == 0:
            continue
        # predict on test data
        logger.debug("    predicting future confirmed cases")
        ypred_1 = xmodel_1.predict(xtest)
        logger.debug("    predicting future deaths")
        ypred_2 = xmodel_2.predict(xtest)

        xout_country = pd.DataFrame(
            {"ForecastId": xtest_id, "PConfirmed": ypred_1, "PDeaths": ypred_2}
        )
        # update forecasts with country data
        xout = pd.concat([xout, xout_country], axis=0)

        # scores
        logger.info(
            f"    Score for confirmed: \n"
            f"      - train: {xmodel_1.score(xtrain, ytrain_1)}, "
            f"test: {xmodel_1.score(xtest, ytest_1)}\n"
            f"    Score for deaths: \n"
            f"      - train: {xmodel_2.score(xtrain, ytrain_2)}, "
            f"test: {xmodel_2.score(xtest, ytest_2)}"
        )

    # merge predictions into testing data 
    Xres = Xtest.merge(xout, on='ForecastId')
    confirmed_mse = ((Xres['Confirmed'] - Xres['PConfirmed']) ** 2).mean()
    deaths_mse = ((Xres['Deaths'] - Xres['PDeaths']) ** 2).mean()
    logger.warning(f"  Confirmed MSE = {confirmed_mse}")
    logger.warning(f"  Deaths MSE    = {deaths_mse}")

    # replace output with preditions
    logger.info("== Post-processing")
    Xres['Confirmed'] = Xres['PConfirmed']
    Xres['Deaths'] = Xres['PDeaths']
    # tag source as predition
    Xres['Source'] = 'prediction'

    # Write to DB
    logger.info("== Write to DB")
    ei.write_data(Xres[ei.DATAPOINTS_COLS].set_index(ei.DATAPOINTS_INDEX), ei.DATAPOINTS_PATH, reset=False)



if __name__ == '__main__':
    fire.Fire(xgboost_prediction)
