class UserHoverProfile {
    constructor() {
        this.setEvents();
    }

    setEvents() {
        jQuery(".tooltip.person-profile").hover(function () {
            let id = jQuery(this).data("id");

            if (id) {
                fetch('/api/persons/' + id, {
                    method: 'GET',
                    headers: {
                        'Accept': 'application/json',
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        let person = data;
                        let name = person.user.first_name + " " + person.user.last_name;

                        jQuery(this).find(".tooltiptext .title").html(name);

                        let properties = "";
                        properties += "<li>" + person.user.email + "</li>";
                        properties += "<li>" + person.phone_number + "</li>";

                        jQuery(this).find(".tooltiptext ul.properties").html(properties);
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
            }
        }, function () {

        });
    }
}
