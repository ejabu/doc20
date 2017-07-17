function filter_by_js (results, domain){
    var new_results;
    new_results = results;
    //Merapikan Domain menjadi string
    if (domain.length > 0) {
        var domain_string=""
        domain.map(function (dom) {
            if (dom[0] !== "|") {
                //Change = to ==
                var operator;
                switch (dom[1]) {
                    case "=":
                        operator = '=='
                        break;
                    default:
                        operator = dom[1]
                }

                //Change to dom[2]
                if (dom[0] == "week_date") {
                    //Change LAST7
                    switch (dom[2]) {
                        case "last4":
                            week = 3;
                            target_date = $.datepicker.formatDate('yy-mm-dd', new Date(new Date().getTime() - (week*60*60*24*7*1000)));
                            condition= '"'+ target_date + '"'
                            break;
                        case "last8":
                            week = 7;
                            target_date = $.datepicker.formatDate('yy-mm-dd', new Date(new Date().getTime() - (week*60*60*24*7*1000)));
                            condition= '"'+ target_date + '"'
                            break;
                        default:
                            condition= '"'+ dom[2] + '"'
                    }
                }
                else {
                    condition = dom[2]
                }



                domain_string+="el."+dom[0]+" "+ operator +" "+ condition +" && "
            }

        })
        domain_string = domain_string.slice(0, -4);
        var to_eval = `
                    new_results = _.filter(results, function (el){
                    return $DOMAIN;
                        }
                    );
                    `;
        to_eval = to_eval.replace('$DOMAIN', domain_string);
        // console.log(to_eval);
        eval(to_eval);
    }

    return new_results

}
