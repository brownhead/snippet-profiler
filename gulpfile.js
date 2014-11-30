var gulp = require("gulp");
var minifyHTML = require("gulp-minify-html");
var concat = require('gulp-concat');
var sourcemaps = require('gulp-sourcemaps');
var source = require('vinyl-source-stream');
var browserify = require('browserify');
var tap = require('gulp-tap');
var reactify = require("reactify");

gulp.task("js", function() {
    return browserify({entries: ["./src/static/jsx/main.jsx"], debug: true})
        .transform(reactify)
        .bundle()
        .pipe(source("main.js"))
        .pipe(gulp.dest("src/genfiles/"));
});

gulp.task("minify-html", function() {
    var opts = {comments:true, spare:true}
    return gulp.src("src/static/index.htm")
        .pipe(minifyHTML(opts))
        .pipe(gulp.dest("src/genfiles/"));
});

gulp.task("watch", function() {
    gulp.watch("src/static/**", ["js", "minify-html"]);
});
