function fill_in_bgg_data() {
    // List all ids of paragraphs
    var allElements = document.getElementsByTagName("p");
    for (var i = 0, n = allElements.length; i < n; ++i) {
        var el = allElements[i];

        // If the id is that of a game, fetch data
        if (el.id && el.id.startsWith('bgg_data_')) {
            pos = el.id.lastIndexOf('_');
            bgg_id = el.id.substring(pos+1);

            // TODO: make this async
            var content = 'BGG id not set in DB.';
            if (bgg_id > 0) {
                // Call BGG API for that ID
                bgg_xml_data = bgg_data_for(bgg_id);

                // Extract interesting stuff
                rating = bgg_rating(bgg_xml_data);
                opt_players = bgg_opt_players(bgg_xml_data);
                weight = bgg_weight(bgg_xml_data);

                content = `
                    - Rating: ${rating}<br/>
                    - Best player count: ${opt_players}<br/>
                    - Weight: ${weight}<br/>
                `;

                // Thumbnail
                image_url = bgg_thumbnail(bgg_xml_data);
                thumbnail = document.createElement('img');
                thumbnail.src = image_url;
                document.getElementById(el.id).insertAdjacentElement('beforebegin', thumbnail)
            }

            document.getElementById(el.id).innerHTML = content;
        }

    }
}

function bgg_data_for(bgg_id) {
    var request = new XMLHttpRequest();
    request.open("GET", `https://boardgamegeek.com/xmlapi2/thing?id=${bgg_id}&stats=1`, false);
    request.send();

    parser = new DOMParser();
    xmlDoc = parser.parseFromString(request.responseText, "text/xml");

    return xmlDoc;
}

function bgg_rating(bgg_xml_data) {
    value = bgg_xml_data.querySelector("average").getAttribute('value');
    return Math.round(value * 10) / 10;
}

function bgg_opt_players(bgg_xml_data) {
    results = bgg_xml_data.querySelectorAll("results");

    best_numplayers = 0;
    best_numplayers_votes = -1;

    results.forEach(element => {
        numplayers = element.getAttribute('numplayers');
        if (numplayers == null) return;

        votes_count = Number(element.querySelector('result').getAttribute('numvotes'));
        if (votes_count > best_numplayers_votes) {
            best_numplayers_votes = votes_count;
            best_numplayers = numplayers;
        }
    });

    return best_numplayers;
}

function bgg_weight(bgg_xml_data) {
    value = bgg_xml_data.querySelector("averageweight").getAttribute('value');
    return Math.round(value * 10) / 10;
}

function bgg_thumbnail(bgg_xml_data) {
    value = bgg_xml_data.querySelector("thumbnail").innerHTML;
    return value;
}
