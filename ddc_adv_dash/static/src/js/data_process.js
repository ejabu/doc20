function filter_by_js (results, domain){
    var new_results;
    new_results = results;
    //Merapikan Domain menjadi string
    if (domain.length > 0) {
        var domain_string=""
        domain.map(function (dom) {
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
                condition= '"'+ dom[2] + '"'
            }
            else {
                condition = dom[2]
            }



            domain_string+="el."+dom[0]+" "+ operator +" "+ condition +" && "
        })
        domain_string = domain_string.slice(0, -4);
        // var to_eval =
        // `
        // results=results.filter(function (el) {
        //     console.log(el.count);
        //     return $DOMAIN;
        // });
        // `
        var to_eval =
        `
        new_results = _.filter(results, function (el){
            return $DOMAIN;
            }
        );
        `
        to_eval = to_eval.replace('$DOMAIN', domain_string);
        eval(to_eval);
    }

    console.log('results after eval');
    console.log(results);
    console.log(new_results);

}


// fn1()
