var Documents = Backbone.Collection.extend({
  url: '/api/documents',
  parse: function(data) {
    return data.results;
  }
});
// An example Backbone application contributed by
// [Jérôme Gravel-Niquet](http://jgn.me/). This demo uses a simple
// [LocalStorage adapter](backbone.localStorage.html)
// to persist Backbone models within your browser.

// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

  var Document = Backbone.Model.extend({

    defaults: function() {
      return {
        correspondent: "",
        title: ""
      };
    }

  });

  var DocumentList = Backbone.Collection.extend({

    // Reference to this collection's model.
    model: Document,
    url: '/api/documents',
    parse: function(data) {
      return data.results;
    }

  });

  var Documents = new DocumentList;

  var DocumentView = Backbone.View.extend({

    tagName:  "li",

    // Cache the template function for a single item.
    template: _.template($('#document-template').html()),

    // The DOM events specific to an item.
    // events: {
    //   "click .toggle"   : "toggleDone",
    //   "click a.destroy" : "clear",
    //   "keypress .edit"  : "updateOnEnter",
    //   "blur .edit"      : "close"
    // },

    // The TodoView listens for changes to its model, re-rendering. Since there's
    // a one-to-one correspondence between a **Todo** and a **TodoView** in this
    // app, we set a direct reference on the model for convenience.
    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      // this.listenTo(this.model, 'destroy', this.remove);
    },

    // Re-render the titles of the todo item.
    render: function() {
      this.$el.html(this.template(this.model.toJSON()));
      this.$el.toggleClass('done', this.model.get('done'));
      this.input = this.$('.edit');
      return this;
    }

  });

  var App = new DocumentView;

});
