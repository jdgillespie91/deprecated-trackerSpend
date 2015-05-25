# What do I plan on building in the future?

## In short

* Add tests.
* Build summary reports.
* Build forecasting reports.
* Centralise logging.
* Determine deployment procedure.
* Improve error handling.

## In more detail

### Building summary reports.

I would like to build reports that detail show much I've spent in a given month, how much I have left to spend and how much I have left to spend after taking into account fixed expenditure (things like rent).

I expect to build these reports by calling psql from within a Python script. I would like to incorporate visualisation of these reports but perhaps a proof-of-concept would be simply to email out some numbers.

### Building forecasting reports.

I would like to build reports that programatically predict my future spending. I realise that the various categories by which I group my spend have different levels of predictability. Some will remain fixed, others will vary by only a small amount, some may be seasonal, and so on. I'd like to build prediction methods that automatically account for this.

Note that this will be an exercise in forecasting since I'll be able to use the infrastructure from the summary reports to actually send these reports out.
