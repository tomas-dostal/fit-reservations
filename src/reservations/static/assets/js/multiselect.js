class Multiselect {
    id = "";
    description = "";

    constructor(id, description = "Zvolte možnost") {
        this.id = id;
        this.description = description;

        jQuery(document).ready(function () {
            // JQuery multiselect frontend
            jQuery('#' + id).multiselect({
                columns: 1,
                search: true,
                placeholder: description,
                noneSelectedText: description,
                selectedText: '# vybráno',
            });
        });
    }
}

class AjaxMultiselect extends Multiselect {
    ajaxAction = "/api/";
    attrName = "";

    constructor(id, ajaxAction, attrName, description = "Zvolte možnost") {
        super(id, description);

        this.ajaxAction = ajaxAction;
        this.attrName = attrName;

        let obj = this;

        jQuery(document).ready(function () {
            // On value changed event handler.
            jQuery("#" + id).change(obj.valueChanged);
        });
    }

    valueChanged = e => {
        // Get new field value.
        let newValue = jQuery("#" + this.id).val();

        // Create request object.
        let data = {};
        data[this.attrName] = newValue;

        // Get CSRF token
        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(this.ajaxAction, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                //console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

}
