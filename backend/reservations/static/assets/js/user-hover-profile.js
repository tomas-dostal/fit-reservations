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
                        let name = person.name + " " + person.surname;

                        jQuery(this).find(".tooltiptext .title").html(name);
                        // TODO add more
                    })
                    .catch((error) => {
                        console.error('Error:', error);
                    });
            }
        }, function () {

        });
    }
}
