// -*- coding: utf-8 -*- vim: sts=4 sw=4 si et
// Wir achten Ihre Privatsphäre - keine Weitergabe der Daten an etwaige
// Werbenetzwerke, Google etc.!
if (! Date.now) {
    Date.now = function () {
        return new Date().getTime();
    }
}

var UnitraccAds = (function () {
    var data = {},
        global = {},
        index = {},
        container = {},
        preloaded = {},
        timeout = {};

    var next_of = function(top, current, step) {
        // step darf weder undefined noch 0 sein ...
        // (negativ auch nicht, aber das prüfen wir hier nicht)
        var val = current + (step || 1);
        if (val >= top) {
            return val % top;
        }
        return val;
    }

    // Gib eine zufällige Ganzzahl zurück mit 0 <= N < max
    var getRandomInt = function (max) {
        return Math.floor(Math.random() * (max + 1));
    }
    
    // die Werbung <relation> weiterschalten
    var switch_ad = function (relation, reload) {
        var old_idx = index[relation],
            adconfig = data[relation],
            adlist = adconfig.ads,
            adlength = adlist.length,
            adnumber = adconfig.number,
            cache_timeout = timeout[relation],
            new_content = [],
            n = 0,
            now = Date.now();
        if (reload === undefined) {
            reload = (cache_timeout && now > cache_timeout);
        }
        if (reload) {
            $.ajax({
                url: '/@@advertisement/get_ads_json',
                data: {relation: relation,
                       lang: adconfig.lang
                       },
                success: function (data, status, XHR) {
                    adconfig[relation] = data;
                },
                error: function (jqXhr, textstatus, error) {
                    if (console && console.log) {
                        console.log(error);
                    }
                },
                complete: function (jqXhr, textStatus) {
                    timeout[relation] = Date.now() + global['lifetime_ms'];
                    // direkter Aufruf leider nicht möglich - wir befinden uns
                    // mitten in der Konstruktion eben dieser Funktion:
                    window.setTimeout('UnitraccAds.switch_ad("'+relation+'", false)', 10);
                }
            })
            return;
        } else {
            while (n < adnumber) {
                idx = next_of(adlength, old_idx);
                new_content.push(make_ad(adlist[idx]));
                if (idx !== old_idx) {
                    old_idx = idx;
                    index[relation] = idx;
                } else {
                    // wir haben geleert; also Abbruch erst hier,
                    // um notfalls dasselbe Element wieder zu erzeugen:
                    break;
                }
                n += 1;
            }
            if (n) {
                container[relation]
                    .empty()
                    .append(new_content)
                    .parent()
                    .show();
            } else {
                container[relation]
                    .empty()
                    .parent()
                    .hide();
            }
        }
    }

    // veröffentlichte Funktion: macht die "Relation" bekannt
    // und sorgt für den periodischen Austausch (switch_ad)
    // bzw. das Neuladen der Konfiguration (reload).
    var register = function (config) {
        var relation = config['relationship'],
            lifetime_ms = config['lifetime_ms'];
        global['reload_ms'] = config['reload_ms'];
        global['lifetime_ms'] = config['lifetime_ms'];
        global['alt'] = config['alt'];
        data[relation] = config;
        container[relation] = $('#ads-'+relation+' .ads-array');
        // Cache-Timeout: 
        timeout[relation] = lifetime_ms
                            ? Date.now() + lifetime_ms
                            : null;
        index[relation] = getRandomInt(config['adslength']);
        switch_ad(relation, false);
        window.setInterval(
                function () {
                    switch_ad(relation);
                }, global['reload_ms']);
    }

    // Erzeuge Werbung, mit oder ohne URL
    var make_ad = function (dic) {
        var url = dic['link2url'],
            src = dic.img_src,
            img = document.createElement('img'),
            elem;
        // Bild laden, aber nicht direkt verwenden:
        preload_img(src);

        img = $('<img />')
            .attr('src', src)
            .attr('alt', global['alt']);
        if (url) {
            elem = $('<a />')
                .attr('href', url)
                .attr('target', '_blank');
            elem.append(img);
            return elem;
        } else {
            return img;
        }
    }

    var preload_img = function (src) {
        if (preloaded[src] === undefined) {
            preloaded[src] = $('<img />')
                .attr('src', src)
                .appendTo('body')
                .hide()
                .delay(10); // dem Browser eine Gelegenheit geben
        }
    }

    // Erzeuge Werbung, mit oder ohne URL
    var make_ad_str = function (dic) {
        var url = dic['link2url'],
            src = dic.img_src,
            img = '<img src="'+src+'" alt="'+global['alt']+'">';
        // Bild laden, aber nicht direkt verwenden:
        preload_img(src);
        if (url) {
            return '<a href="'+url+'" target="_blank">'+img+'</a>';
        } else {
            return img;
        }
    }

    return {'register': register,
            'switch_ad': switch_ad}
})();
