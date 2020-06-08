var app = new Vue({
    el: '#app',
    data: function () {
        return {
            query: '',
            selected: []
        }
    },
    methods: {
        querySearch(queryString, cb) {
            fetch(`http://localhost:5000/searchProperties?query=${encodeURIComponent(queryString)}`)
                .then(res => res.json())
                .then(data => {
                    console.log(data)
                    let suggestions = data.map(property => ({ ...property, value: property['Full Address'] })) // Add value property for autocomplete
                    cb(suggestions)
                }).catch(error => {
                    console.error(error);
                });
        },
        handleSelect(property) {
            fetch(`http://localhost:5000/selectProperty?PIN=${encodeURIComponent(property.PIN)}`, {
                method: 'post',
            }).then(response => {
                console.log(response)
                this.getSelectedProperties()
            }).catch(error => {
                console.error(error)
            });
        },
        handleDelete(id) {
            fetch(`http://localhost:5000/deselectProperty?PIN=${encodeURIComponent(id)}`, {
                method: 'post',
            }).then(response => {
                console.log(response)
                this.getSelectedProperties()
            }).catch(error => {
                console.error(error)
            });
        },
        getSelectedProperties() {
            fetch(`http://localhost:5000/getSelectedProperties`)
                .then(res => res.json())
                .then(data => {
                    console.log(data)
                    this.selected = data
                }).catch(error => {
                    console.error(error)
                });
        }
    },
    mounted() {
        this.getSelectedProperties()
    }
})