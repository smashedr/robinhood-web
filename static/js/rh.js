
secObj = $.parseJSON(securities);
console.log(secObj);
console.log(secObj['AMZN']);
symbols = Object.keys(secObj).join(',');
console.log(symbols);

// setInterval(function() {
    $.ajax({
        type:"GET",
        url:"https://api.robinhood.com/quotes/?symbols="+symbols,
        datatype:"html",
        beforeSend: function( jqXHR ){
            console.log('beforeSend');
        },
        complete: function(){
            console.log('complete');
        },
        success: function(data, textStatus, jqXHR) {
            console.log(data);
            console.log(data.results);
            $.each(data.results, function(idx, stock){
                // $('#' + elementID).val(value);
                console.log(stock);
                s = stock.symbol;
                console.log(s);
                console.log(secObj[s]);
                console.log("Average Buy Price: "+secObj[s]['position']['average_buy_price']);
                $('#last-'+stock.symbol).html(stock.last_extended_hours_trade_price);
            });
        },
        error: function(jqXHR, textStatus, errorThrown ) {
            console.log(jqXHR.responseText);
            // var data = jQuery.parseJSON(jqXHR.responseText);
            // console.log(data);
            // $('#alert-div').append(genAlert(data));
        }
    });
// }, 60000);//time in milliseconds
