container = new Vue({
    el: '#container',
    data: {
        tiles: [],
    },
    methods:{
        getRandomBoard: function(){
            axios({
                method: 'get',
                url: '/api/generate/random',
            })
            .then(response => {
                this.tiles = response.data.board;
                console.log(this.tiles)
            })
            .catch(error => {
                console.log(error)
            });
        },
        getCustomBoard: function(){

        }
    },
    mounted: function(){
        this.getRandomBoard()
    }
})
