var general = new Vue({
  el: "#general",
  delimiters: ['${', '}'],
  data: {
  },
  methods: {
    goHome: function() {
      window.location.href = '/home'
    }
  }
})
