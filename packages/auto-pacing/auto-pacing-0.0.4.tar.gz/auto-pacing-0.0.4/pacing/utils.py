

class Datapoint():
    """
    Class: Datapoint

    Description:
        Represents a datapoint used by the pacing model for predicting the proper adjustment factor

   Params
        @param spend (float) - The spend component of the return on investment calculation for this datapoint.
        @param revenue (float) - The revenue component of the return on investment calculation for this datapoint.
        @param adjustment (float) - Any adjustment factor that was applied to the spend .
    """
    def __init__(self, spend: float, revenue: float, adjustment: float=1.0):
        self.spend = spend
        self.revenue = revenue
        self.deficit = revenue - spend
        self.adjustment_factor = adjustment
        self.efficiency = revenue / spend

class PacingModel():
    """
    Class: Pacing Model

    Description:
        Calculates an adjustment factor for pacing time series predictions. Time series predictions contain small errors
        which compound over time. This is problematic when attempting to hit specific goals. This function
        computes an adjustment factor meant to be an overlaid on top of a time-series forecasted datapoint. This
        factor helps adjust data points to make up for previous prediction errors in order to meet a specific
        performance target. The returned factor is meant to be multiplied to the predicted datapoint.

        The current model is specifically used for meeting return on investment targets.

    Usage:
        pacer = PacingModel()

        #: generate a random revenue value
        daily_revenue = 100 + 100 * 0.2 * np.random.uniform(-1, 1)

        #: generate a daily spend value with the desired simulated efficiency to correct
        daily_spend = 125 + 125 * 0.2 * np.random.uniform(-1, 1)

        #: adjust the spend by the sensitivity factor
        adjusted_spend = daily_spend * sensitivity_factor

        #: create a datapoint for spend / revenue data
        datapoints.append(Datapoint(revenue=daily_revenue, spend=adjusted_spend, adjustment_factor=sensitivity_factor))

        #: compute the adjustment factor for the next iteration
        sensitivity_factor = pacer.predict(datapoints, target_efficiency=1.0)
    """
    def __init__(self):
        pass

    def predict(self, datapoints: [Datapoint], target: float):
        """

        Params
            @param datapoints ([Datapoint]): List of historical datapoints of type Datapoint. This helps the model
                                             predict a proper adjustment using historical data and running deficit from
                                             target.
            @param target (float): Return on investment target

            @return (float): Adjustment meant to be multiplied to the next datapoint.
        """

        total_spend = sum([dp.spend for dp in datapoints])
        total_revenue = sum([dp.revenue for dp in datapoints])

        #: compute total deficit
        accumulated_deficit = total_revenue / target - total_spend

        #: predicted deficit for the upcoming (yet to be realized) datapoint
        predicted_deficit = datapoints[len(datapoints) - 1].revenue / target - datapoints[len(datapoints) - 1].spend / datapoints[len(datapoints) - 1].adjustment_factor

        #: compute adjustment
        sensitivity_factor = 1 + (accumulated_deficit + predicted_deficit) * datapoints[len(datapoints) - 1].adjustment_factor / datapoints[len(datapoints) - 1].spend

        return sensitivity_factor