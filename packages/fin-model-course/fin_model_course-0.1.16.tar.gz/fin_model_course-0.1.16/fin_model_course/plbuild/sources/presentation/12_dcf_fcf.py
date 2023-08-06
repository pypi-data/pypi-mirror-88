import pyexlatex as pl
import pyexlatex.table as lt
import pyexlatex.presentation as lp
import pyexlatex.graphics as lg
import pyexlatex.layouts as ll

import plbuild
from lectures.dcf_fcf.main import get_dcf_fcf_lecture
from lectures.lab_exercises.notes import get_fcf_calculation_lab_lecture, get_simple_forecast_lab_lecture, \
    get_complex_forecast_lab_lecture, get_dcf_tv_lab_lecture
from plbuild.paths import images_path
from pltemplates.frames.model_flowchart import (
    ModelFlowchartFrame,
    real_world_style,
    model_style,
    in_out_style
)
from pltemplates.blocks import LabBlock, InClassExampleBlock
from pltemplates.frames.in_class_example import InClassExampleFrame
from pltemplates.eq_with_variable_defs import EquationWithVariableDefinitions
from pltemplates.hyperlink import Hyperlink
from pltemplates.frames.single_block import SingleBlockDimRevealListFrame
from pltemplates.exercises.dcf_fcf import get_dcf_fcf_calculation_exercise, get_dcf_fcf_simple_forecast_exercise, \
    get_dcf_fcf_complex_forecast_exercise, get_dcf_fcf_tv_exercise
from schedule.main import LECTURE_12_NAME

AUTHORS = ['Nick DeRobertis']
SHORT_TITLE = 'FCF'
SUBTITLE = 'Calculation and Projection'

SHORT_AUTHOR = 'DeRobertis'
INSTITUTIONS = [
    ['University of Florida', 'Department of Finance, Insurance, and Real Estate'],
]
SHORT_INSTITUTION = 'UF'

DOCUMENT_CLASS = lp.Presentation
OUTPUT_LOCATION = plbuild.paths.SLIDES_BUILD_PATH
HANDOUTS_OUTPUT_LOCATION = plbuild.paths.HANDOUTS_BUILD_PATH
TITLE = LECTURE_12_NAME
ORDER = 'S12'


def get_content():
    non_cash_items = [
        'depreciation',
        'amortization',
        'stock-based compensation',
        'impairment charges',
        'gains/losses on investments'
    ]
    non_cash_str = ', '.join(non_cash_items[:-1]) + ', and ' + non_cash_items[-1]
    non_cash_eq = pl.Equation(
        str_eq=f'{pl.Text("Adjustments")} = {" + ".join([str(pl.Text(item)) for item in non_cash_items])}',
    )

    lecture = get_dcf_fcf_lecture()
    fcf_exercise = get_fcf_calculation_lab_lecture().to_pyexlatex()
    simple_ts_exercise = get_simple_forecast_lab_lecture().to_pyexlatex()
    complex_ts_exercise = get_complex_forecast_lab_lecture().to_pyexlatex()
    tv_exercise = get_dcf_tv_lab_lecture().to_pyexlatex()

    return [
        pl.Section(
            [
                lp.DimRevealListFrame(
                    [
                        'There are two main parts to the FCF part of the DCF model',
                        'First is to find all the historical FCFs. This is the straightforward part of '
                        'plugging values into set calculations.',
                        'The more difficult and important part is projecting future cash flows',
                        'We will discuss a variety of approaches for this'
                    ],
                    title='FCF Overview'
                ),
                lp.DimRevealListFrame(
                    [
                        'Free cash flow (FCF) represents cash a company earns after paying for its operations.',
                        'It is not to be confused with net income, which amortizes costs across years and '
                        'includes non-cash expenses',
                        'FCF represents only the cash flows from that year, and so can be a lot more variable than '
                        'net income',
                        'FCF is the actual cash earned, and so it is what we should use for valuation'
                    ],
                    title='What is FCF?'
                ),
                lp.TwoColumnGraphicDimRevealFrame(
                    [
                        'We can follow a simple formula to get FCFs from historical financials',
                        'All we have to do is calculate the formula for each year of historical data',
                        'Each of the components to this calculation besides net income themselves require '
                        'a calculation. In the Historical FCF section we will cover each component.',
                        'The formula is all about reversing the non-cash adjustments to net income'
                    ],
                    graphics=[
                        images_path('fcf-formula.png')
                    ],
                    title='Historical FCFs'
                ),
                lp.DimRevealListFrame(
                    [
                        'The challenge in the FCF model is to project the cash flows',
                        ['There are two main approaches to getting future FCFs:', pl.Underline('forecast the FCFs'),
                         'and', pl.Underline('forecast the financial statements.')],
                        'Forecasting FCFs is much easier but is not as accurate, both due to lack of granularity and '
                        'due to typically uneven FCFs',
                        ['We will use', pl.Underline('time-series methods'), 'to forecast the financial statements, '
                         'either in the', pl.Underline('levels'), 'of the item, the', pl.Underline('growth'),
                         'of the item, or as a', pl.Underline('percentage of another item')]
                    ],
                    title='Forecasting FCFs'
                )
            ],
            title='Overview'
        ),
        pl.Section(
            [
                SingleBlockDimRevealListFrame(
                    [
                        'Non-cash expenses is just the sum of all items on the income statement that do not '
                        'affect cash.',
                        f'This includes {non_cash_str}'
                    ],
                    block_contents=[non_cash_eq],
                    block_title='Calculate Non-Cash Expenses',
                    title='Non-Cash Expenses'
                ),
                SingleBlockDimRevealListFrame(
                    [
                        'Net Working Capital (NWC) represents cash actively tied up in daily transactions',
                        'Cacluating the change in NWC requires information from this period '
                        'as well as last period.',
                        'First, calculate the NWC in each period using accounts receivable, '
                        'inventory, and accounts payable.',
                        "Then, take the difference between this period's NWC and last to get the change"
                    ],
                    block_contents=[
                        pl.Equation(
                            str_eq=rf'\Delta{pl.Text("NWC")} = {pl.Text("NWC")}_t - {pl.Text("NWC")}_{{t-1}}',
                            inline=False
                        ),
                        pl.Equation(
                            str_eq=rf'{pl.Text("NWC")} = {pl.Text("Accounts Receivable")} + {pl.Text("Inventory")} '
                                   rf'- {pl.Text("Accounts Payable")}',
                            inline=False
                        )
                    ],
                    block_title='Calculate Change in NWC',
                    title='Change in Net Working Capital'
                ),
                SingleBlockDimRevealListFrame(
                    [
                        'Capital Expenditures (CapEx) are outlays for fixed assets which get used over time, such '
                        'as buildings or machinery.',
                        'The change in Property, Plant and Equipment from the balance sheet can be used to estimate '
                        'CapEx.',
                        'Then you just need to add back the current depreciation & amortization, as they decreased '
                        'PPE even though no cash exchanged hands'
                    ],
                    block_contents=[
                        pl.Equation(
                            str_eq=fr'{pl.Text("CapEx")} = \Delta{pl.Text("PPE")} + '
                                   fr'{pl.Text("Depreciation & Amortization")}',
                            inline=False
                        )
                    ],
                    block_title='Calculate CapEx',
                    title='Capital Expenditures'
                ),
                SingleBlockDimRevealListFrame(
                    [
                        'Again, the FCF formula takes net income and reverses the non-cash adjustments',
                        'Add back the non-cash expenses because no actual cash was spent',
                        'Decrease by the change in NWC as an increase means additional cash was used for operations',
                        'Decrease by CapEx because this cash was spent for a new building, machinery, etc.'
                    ],
                    block_contents=[
                        pl.Equation(
                            str_eq=fr'{pl.Text("FCF")} = {pl.Text("Net Income")} + {pl.Text("Non-Cash Expenses")} - '
                                   fr'\Delta{pl.Text("NWC")} - {pl.Text("CapEx")}',
                            inline=False
                        )
                    ],
                    block_title='Calculating FCF',
                    title='Put it All Together'
                ),
                InClassExampleFrame(
                    [
                        'Go to the course site and download the files in Historical FCF',
                        'There should be a Jupyter notebook as well as a data file',
                        'We will go through a couple approaches to calculating FCFs in Python.'
                    ],
                    title='Example for Calculating FCFs',
                    block_title='Two Ways to Calculate FCFs in Python'
                ),
                fcf_exercise.presentation_frames(),
            ],
            title='Calculating Historical Free Cash Flows',
            short_title='Historical FCF',
        ),
        pl.Section(
            [
                lp.DimRevealListFrame(
                    [
                        pl.TextSize(-1),
                        'As mentioned in the intro, we will use time-series methods on the levels of the item, '
                        'the growth of the item, or as a percentage of another item',
                        'Time-series methods are about numerically estimating future values based on past values',
                        'Levels mean we forecast the numbers of the item itself, e.g. sales was 1M two years ago and '
                        '1.5M last year so we feed those numbers into our time-series model and predict 2M for the '
                        'next year',
                        'Growth means to first calculate the historical growth rate of the item, then forecast that. '
                        'E.g. sales grew 10% two years ago and 8% last year so we expect it to grow 6% this year',
                        'Percentage of item methods link an item to another item. E.g. setting cost of goods sold to '
                        '60% of sales. That percentage still needs to be forecasted',
                        "Any forecast can be adjusted by the analyst's qualitative projections of the future. The "
                        "forecast method may also have to be chosen with the qualitative analysis in mind"
                    ],
                    title='Overview of the Methods'
                ),
                lp.TwoColumnGraphicDimRevealFrame(
                    [
                        'Time-series methods seek to predict the future using the past',
                        'There is a large variety of possible time-series models to use for forecasting',
                        'They each use different characteristics of the past to assist in predicting the future'
                    ],
                    graphics=[
                        images_path('time-series-linear-plot.png')
                    ],
                    title='What Are Time-Series Methods?'
                ),
                lp.DimRevealListFrame(
                    [
                        ['The simplest models are to use the', pl.Underline('average of historical values'), 'or the',
                         pl.Underline('most recent value'), 'as the prediction for all future values'],
                        ['A more realistic model will also include estimating the', pl.Underline('trend'),
                         f'or {pl.Underline("growth")} of the historical values and applying that to the future'],
                        'More advanced models use autoregressive terms (recent values predict future values), moving '
                        'average terms (recent errors predict future values), or conditional heteroskedasticity terms '
                        '(changing variance over time)',
                        'Examples of these advanced models include AR, MA, ARMA, ARCH, GAM, and many more'
                    ],
                    title='What are the Time-Series Models?'
                ),
                lp.DimRevealListFrame(
                    [
                        'The choice of a time-series model will depend on the amount of data, the frequency of the '
                        'data, and the historical patterns in the data',
                        'If the data is historically constant or expected to be constant in the future, using the '
                        'average or most recent value should be enough',
                        "If the data follows a defined trend or growth and doesn't have historical patterns, "
                        "then using the "
                        "trend or growth models should be enough",
                        'If there are historical patterns in the data, such as seasonality, then more advanced '
                        'models are required.'
                    ],
                    title='Which Time-Series Model to Use?'
                ),
                lp.DimRevealListFrame(
                    [
                        ['The best place to start is to', pl.Underline('examine the history'), 'either by a plot',
                         'or just by looking at the numbers if you only have a few'],
                        ['Based on the amount of historical data, any perceived patterns in the historical data, '
                         'and any qualitative knowledge of the data,', pl.Underline('choose a time-series model.')],
                        [pl.Underline('Fit'), 'the time-series model on historical data, then', pl.Underline('predict'),
                         'the future values using the fitted model'],
                        ['Finish by', pl.Underline('examining the forecast'), 'to ensure it worked as intended, ',
                         'typically via a plot.']
                    ],
                    title='Steps to Forecasting'
                ),
                lp.DimRevealListFrame(
                    [
                        'When we forecast levels, just use the forecasted values and you are done',
                        'When we forecast growth, calculate the historical growth, run the forecast on that, then '
                        'apply the predicted future growth from the final historical period to generate '
                        'the forecasted levels',
                        'For percentage of item methods, calculate the historical percentage of the item, '
                        'forecast future item percentages, then use these in combination with '
                        'the forecast of the referenced item to generate the prediction',
                        'E.g. use the average approach to say historically COGS was 40% of sales, and so estimate '
                        'COGS as 40% of sales going forward. Multiply the forecasted sales by 40% to get the COGS',
                    ],
                    title='What to Forecast?'
                )
            ],
            title='Approaches to Forecasting',
            short_title='Forecasting Overview'
        ),
        pl.Section(
            [
                SingleBlockDimRevealListFrame(
                    [
                        [
                            pl.Bold('Fit:'),
                            'To fit the historical average model, take an average of the historical values'
                        ],
                        [
                            pl.Bold('Predict:'),
                            'To predict, use that average value for all future values'
                        ]
                    ],
                    [
                        EquationWithVariableDefinitions(
                            r'y_{T + n} = \frac{1}{T} \sum_{t=0}^T y_t + \epsilon_t',
                            [
                                '$t$: Current time period',
                                '$T$: Last time period of historical data',
                                '$y_t$: The current value of the data',
                                '$y_T$: The last historical value of the data',
                                '$n$: Number of periods forecasted'
                            ]
                        )
                    ],
                    title='Using the Historical Average Model',
                    block_title='Historical Average Model'
                ),
                SingleBlockDimRevealListFrame(
                    [
                        [
                            pl.Bold('Fit:'),
                            'To fit the most recent value model, take the latest value.'
                        ],
                        [
                            pl.Bold('Predict:'),
                            'To predict, use that latest value for all future values'
                        ]
                    ],
                    [
                        pl.Equation(str_eq=r'y_t = y_{t-1} + \epsilon_t', inline=False)
                    ],
                    title='Using the Recent Value Model',
                    block_title='Recent Value Model'
                ),
                SingleBlockDimRevealListFrame(
                    [
                        [
                            pl.Bold('Fit:'),
                                [
                                    'Run an OLS regression with a constant and time as the independent variable, '
                                    'where time is measured in number of periods since the beginning',
                                ],
                        ],
                        [
                            pl.Bold('Predict:'),
                                [
                                    r'For each $t$ you want to predict, calculate $a + \beta t$',
                                ],
                        ]
                    ],
                    [
                        pl.Equation(str_eq=r'y_t = a + \beta t + \epsilon_t', inline=False)
                    ],
                    title='Using the Trend Model',
                    block_title='Trend Model'
                ),
                SingleBlockDimRevealListFrame(
                    [
                        [
                            pl.Bold('Fit:'),
                            [
                                'Calculate the compounded annual growth rate (CAGR) as',
                                pl.Equation(str_eq=r'\frac{y_T}{y_0}^{\frac{1}{n}} - 1')
                            ]
                        ],
                        [
                            pl.Bold('Predict:'),
                            ['Calculate future periods by compounding CAGR on the latest historical period',
                            pl.Equation(str_eq=rf'y_{{T + f}} = y_T * (1 + {pl.Text("CAGR")})^f')]
                        ]
                    ],
                    [
                        pl.Equation(str_eq=r'y_{{T + f}} = y_T * (\frac{y_T}{y_0}^{\frac{1}{n}})^f', inline=False)
                    ],
                    title='Using the CAGR Model',
                    block_title='CAGR'
                ),
                InClassExampleFrame(
                    [
                        'Go to the course site and download the files in Examples > DCF > Forecasting > Simple',
                        'There should be a Jupyter notebook as well as two Excel files. Place these all in the '
                        'same folder',
                        'We will walk through "Sales COGS Forecasted.xlsx" to show forecasting in Excel, and '
                        '"Forecast Sales COGS Simple.ipynb" for forecasting in Python. "Sales COGS.xlsx" '
                        'contains the source data'
                    ],
                    title='Forecasting Simple Time-Series in both Excel and Python',
                    block_title='Example for Simple Time-Series Forecasting'
                ),
                simple_ts_exercise.presentation_frames(),
                InClassExampleFrame(
                    [
                        'Go to the course site and download "Forecasting Financial Statements.ipynb"',
                        f'We will walk through using {pl.Monospace("finstmt")} to forecast financial statements '
                        'using simple time-series models',
                    ],
                    title='Forecasting Financial Statements with Simple Time-Series in Python',
                    block_title='Use finstmt for Financial Statement Forecasting'
                ),
            ],
            title='Forecasting Simple Time-Series',
            short_title='Simple Forecast'
        ),
        pl.Section(
            [
                lp.TwoColumnGraphicDimRevealFrame(
                    [
                        "Shown to the left is Walmart's quarterly sales",
                        'You can see that a plain trend line is never going to accurately forecast these values',
                        'Advanced time-series models can capture these characteristics easily, and many more patterns'
                    ],
                    graphics=[
                        images_path('time-series-plot.png')
                    ],
                    graphics_on_right=False,
                    title='Why Does it get so Complicated?'
                ),
                lp.TwoColumnGraphicDimRevealFrame(
                    [
                        ['There is a distinct', pl.Bold('seasonality'), "to Walmart's quarterly sales"],
                        'The time-series model used to create the plot on the prior slide split the history into '
                        'two parts: a trend component and an annual seasonality component',
                        "Walmart's sales are high at the end of January and neutral for the other quarters",
                        'By plotting components of the time-series model, the analyst can gain a greater understanding '
                        'of the business.'
                    ],
                    graphics=[
                        images_path('time-series-plot-components.png')
                    ],
                    title='Explaining Seasonal Data'
                ),
                lp.DimRevealListFrame(
                    [
                        "So you've determined a trend alone will not fit the historical data. What are next steps?",
                        ['Generally fitting the best time-series model is an involved process which requires '
                         'substantial knowledge of how the models work, see',
                         Hyperlink(
                             'https://www.seanabu.com/2016/03/22/time-series-seasonal-ARIMA-model-in-python/',
                             'this blog post'
                         ), 'for details'],
                        ['An easier version is to use an OLS regression model with time and dummy variables '
                        'for month of year, etc., we can call this the ', pl.Underline('quarterly seasonal trend model.')],
                        ['The easiest version is to let time-series software, such as',
                         Hyperlink('https://facebook.github.io/prophet/docs/quick_start.html', 'prophet'),
                         'make the choice for you']
                    ],
                    title='Predicting Complex Time-Series'
                ),
                SingleBlockDimRevealListFrame(
                    [
                        [
                            pl.Bold('Fit:'),
                            'Create dummy variables for the quarters, then run an OLS regression with the number '
                            'of time periods as well as the four dummy variables as the $X$ variables'
                        ],
                        [
                            pl.Bold('Predict:'),
                            r'For each $t$ you want to predict, calculate $a + \beta t$ adding the appropriate '
                            r'dummy for the quarter of the period.'
                        ]
                    ],
                    [
                        pl.Equation(str_eq=r'y_t = a + \beta_t t + \beta_{d1} D1 + \beta_{d2} D2 + '
                                           r'\beta_{d3} D3 + \beta_{d4} D4  + \epsilon_t', inline=False)
                    ],
                    title='Using the Quarterly Seasonal Trend Model',
                    block_title='Quarterly Seasonal Trend Model'
                ),
                InClassExampleFrame(
                    [
                        'Go to the course site and download the files in Examples > DCF > Forecasting > Complex',
                        'There should be a Jupyter notebook as well as two Excel files. Place these all in the '
                        'same folder',
                        'We will walk through "Forecasting Quarterly Financial Statements.ipynb" to show forecasting '
                        'in Python using both the Quarterly Seasonal Trend Model and the automated software approach.'
                    ],
                    title='Forecasting Complex Time-Series in Python',
                    block_title='Example for Complex Time-Series Forecasting'
                ),
                complex_ts_exercise.presentation_frames(),
            ],
            title='Forecasting Complex Time-Series',
            short_title='Complex Forecast'
        ),
        pl.Section(
            [
                lp.DimRevealListFrame(
                    [
                        'As mentioned in the intro, we can either directly forecast FCFs, or forecast the financial '
                        'statements, then calculate future FCFs from the future financial statements',
                        "Forecasting FCFs doesn't allow the analyst control over individual "
                        "line items. Therefore it is generally preferred to forecast financial statements.",
                        'If you have a short amount of time to put together the model, it can make sense as it is '
                        'less steps and it requires less knowledge of the company.',
                        'It can also make sense to do a FCF forecast alongside the financial statement forecast, as '
                        'a check on your valuation.'
                    ],
                    title='What to Forecast?'
                ),
                lp.DimRevealListFrame(
                    [
                        'Assuming you are going with forecasting financial statements, you should '
                        'forecast only line items which cannot be calculated from other line items',
                        'For example, sales, COGS, SG&A should be forecasted, not operating profit',
                        'You should set your model up so that these calculatable items are calculated '
                        'in the historicals, then carry that through to the forecasted',
                        'Set items as a percentage of other items when it is logical that they should '
                        'scale together. For example, interest expense should be forecasted as a percentage '
                        'of total debt, as if the company takes on more debt, interest expense should increase '
                        'proportionally',
                    ],
                    title='Which Line Items to Forecast?'
                ),
                lp.DimRevealListFrame(
                    [
                        'Despite forecasting line items individually, you must attempt to keep the balance sheet '
                        'balanced in the future',
                        'If your forecast shows assets growing to be much greater than liabilities and equity, '
                        'that implies that the company will need to raise additional funds to finance the '
                        'growth in the assets. Usually increasing debt is the solution.',
                        'If your forecast shows assets lower than liabilities and equity, it means that the profits '
                        'or other sources of funds are not being properly allocated to the assets side. Usually '
                        'increasing cash is the solution',
                    ],
                    title="Don't Be Out of Balance"
                ),
                lp.DimRevealListFrame(
                    [
                        pl.TextSize(-1),
                        'The general process is to run your forecasts, then use another approach to adjust either '
                        'cash or debt to make the balance sheet balance. ',
                        'These adjusted values are called "plugs" because we are "plugging" in whatever makes the '
                        'forecast valid',
                        'To make the adjustment in Excel, calculate the absolute value of the '
                        'difference between assets and liabilities + '
                        'equity, then use goal seek (single year forecast) or solver (multi-year forecast) '
                        'to minimize the value',
                        'In Python, the steps would be similar, only using scipy minimize instead of solver, '
                        'but finstmt handles this automatically for you. When you run a forecast, it will balance '
                        'the balance sheet without any further action from you. You can change how accurate it '
                        'is by setting bs_diff_max and you can change which line items are used as plugs '
                        'in the forecast config',
                    ],
                    title='Balancing the Balance Sheet'
                )
            ],
            title='Forecasting Free Cash Flows',
            short_title='Future FCFs'
        ),
        pl.Section(
            [
                lp.DimRevealListFrame(
                    [
                        'As mentioned in the intro to the DCF model, we can value any asset by taking the present value '
                        'of future cash flows',
                        'These forecasted FCFs represent the future cash flows for the company',
                        'But we have a limited forecast period, beyond which forecasts are getting too innaccurate, '
                        'typically 5 years at most. So what happens after 5 years? The company will probably still be '
                        'earning FCFs in the future.',
                        ['We can calculate a', pl.Bold('terminal value'), 'for the company, which is an estimate of '
                         'how much the company would be sold for if it was sold at the end of the forecast period. '
                         'In other words, it is the future predicted enterprise value.']
                    ],
                    title='What we use FCFs For'
                ),
                lp.DimRevealListFrame(
                    [
                        'The terminal value is an enterprise value at the end of the forecast period. But the bulk of '
                        'the DCF model is getting to an enterprise value, so we have to use a different method '
                        'to estimate the terminal value otherwise we would have an infinitely nested DCF model that could '
                        'never be solved.',
                        ['The two common methods for estimating the terminal value in a DCF model are',
                         pl.Underline('exit multiples'), 'and', pl.Underline('perpetuity growth')],
                        'The exit multiple method uses current values of valuation ratios and applies them to the '
                        'future financials',
                        'The perpetuity growth method assumes that the FCFs will grow at a constant rate after the '
                        'final forecast period.'
                    ],
                    title='How to Get the Terminal Value'
                ),
                lp.DimRevealListFrame(
                    [
                        'There are typically publicly available valuation ratios for public companies such as EV/EBIT, '
                        'EV/EBITDA, EV/Sales, EV/FCF, and P/E',
                        'The idea behind this approach is to use those ratios applied to your final period projected '
                        'financials.',
                        'Each ratio will yield a different terminal value, leading to a different final stock price '
                        'in your model. It is typical to report results with the different measures to get a range.',
                        'For all the EV ratios, multiply the statement item by the ratio to get the EV, then adjust the '
                        'EV using final forecasted values to get the equity value and stock price',
                        'For P/E, calculate final period earnings per share and multiply by the ratio to get the '
                        'stock price'
                    ],
                    title='Finding the Terminal Value via Exit Multiples'
                ),
                lp.DimRevealListFrame(
                    [
                        'The perpetuity growth model follows the same mathematics as the dividend discount model',
                        "We just assume that the last period's FCF continues to grow at some terminal growth rate "
                        "which we set.",
                        pl.Equation(str_eq=r'TV = \frac{FCF (1 + g)}{WACC - g}'),
                        ['The stock price is', pl.Underline('highly'), 'sensitive to the choice of terminal growth '
                         'rate, so there should absolutely be sensitivity analysis and Monte Carlo simulations varying '
                         'it'],
                        'Typical terminal growth rates are around 3%, approximately GDP growth rate'
                    ],
                    title='Finding the Terminal Value via Perpetuity Growth'
                ),
                lp.DimRevealListFrame(
                    [
                        'The last step to get the current enterprise value is to combine the FCFs with the TV',
                        'The TV cash flow should come in the final forecast period, such that the final cash flow '
                        'is $FCF + TV$',
                        'Take the NPV of the cash flows, including the TV',
                        'Follow the adjustments described in the intro lecture to get the stock price from that'
                    ],
                    title='Finding EV Using TV and FCFs'
                ),
                pl.TextSize(-2),
                tv_exercise.presentation_frames(),
                pl.TextSize(0)
            ],
            title='Using the Forecasted FCFs in the DCF Model',
            short_title='Valuation'
        ),

        pl.PresentationAppendix(
            [
                lecture.pyexlatex_resources_frame,
                fcf_exercise.appendix_frames(),
                simple_ts_exercise.appendix_frames(),
                complex_ts_exercise.appendix_frames(),
                tv_exercise.appendix_frames(),
            ]
        )
    ]


DOCUMENT_CLASS_KWARGS = dict(
    nav_header=True,
    toc_sections=True
)
OUTPUT_NAME = TITLE
