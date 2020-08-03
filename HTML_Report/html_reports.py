import os
import logging

logger = logging.getLogger(__name__)


class HtmlReportBuilder:
    def __init__(self):
        pass

    @staticmethod
    def __html_report(start_time, duration, summary, table_body):
        html_template = """
                <!DOCTYPE html>
    <html>
    <head>
        <title>API Test Run Result</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7" crossorigin="anonymous">
    </head>
    <body>
        <div class="container">
            <div class="row">
                <div class="col-xs-12">
                    <h2 class="text-capitalize">API Test Run Result</h2>
                    <p class='attribute'><strong>Start Time: </strong>""" + start_time + """</p>
                    <p class='attribute'><strong>Duration: </strong>""" + duration + """</p>
                    <p class='attribute'><strong>Summary: </strong>""" + summary + """</p>
                </div>
            </div>
            <div class="row">
                <div class="col-xs-12 col-sm-10 col-md-10">
                    <table class='table table-hover table-responsive'>
                        <thead>
                            <tr>
                                <th>Zomato API Automation</th>
                                <th>Status</th>
                                <th></th>
                            </tr>
                        </thead>
                    <tbody>""" + table_body + """</table>
                </div>
            </div>
        </div>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>
        <script type="text/javascript">
            $(document).ready(function(){
                $('td').on('click', '.btn', function(e){
                    e.preventDefault();
                    e.stopImmediatePropagation();
                    var $this = $(this);
                    var $nextRow = $this.closest('tr').next('tr');
                    $nextRow.slideToggle("fast");
                    $this.text(function(i, text){
                        if (text === 'View') {
                            return 'Hide';
                        } else {
                            return 'View';
                        };
                    });
                });
            });
        </script>
    </body>
    </html>"""
        return html_template

    def get_report(self, **kwargs):
        body_template = """<tr class={0}>
                                    <td class="col-xs-10">{1}</td>
                                    <td class="col-xs-1">
                                        <span class="label label-{2}" style="display:block;width:40px;">{3}</span>
                                    </td>
                                    <td class="col-xs-1">
                                        <button class="btn btn-default btn-xs">View</button>
                                    </td>
                                </tr>
                                <tr style="display:none;">
                                    <td class="col-xs-9" colspan="3"><p style="color:{4};">{5}</p>
                                    <p style="color: 'blue';">{6}</p>
                                    </td>
                                </tr>"""
        table_body = """"""
        _pass, _fail = 0, 0
        for _report in kwargs['test_cases']:
            if _report['result'] == 'Pass':
                _cls = 'success'
                _sts = 'Pass'
                _col = 'green'
                _text = _report['test_detail']
                _pass += 1
            else:
                _cls = 'warning'
                _sts = 'Fail'
                _col = 'maroon'
                _text = _report['failure_reason']
                _fail += 1
            table_body = table_body + body_template.format(_cls, _report['summary'], _cls, _sts, _col, _text,
                                                           _report['response_json_loc'])
        _total = _pass + _fail
        start_time = kwargs['start_time']
        end_time = kwargs['end_time']
        duration = end_time - start_time
        summary = "Total: {0}, Pass: {1}, Fail: {2}".format(str(_total), str(_pass), str(_fail))
        with open(os.getcwd() + '/API_TEST_REPORT.html', 'w') as _html_file:
            _html_file.write(self.__html_report(str(start_time), str(duration), summary, table_body))
            _html_file.close()
        logger.info(summary)
