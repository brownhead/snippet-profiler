var React = require("react");

var SnippetEditor = React.createClass({
    render: function() {
        var name = `snippet-javascript[${this.props.index}]`;

        return <div className="snippet-editor">
            <label>Javascript <textarea name={name} /></label>
        </div>;
    },
});

module.exports = React.createClass({
    render: function() {
        return <div className="create-group-screen">
            <h2>New Snippet Group</h2>
            <label>Title <input type="text" name="title" /></label>
            <label>Description <textarea name="description" /></label>
            <SnippetEditor index={1} />
        </div>;
    },
});
