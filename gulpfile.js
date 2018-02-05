var gulp = require('gulp');
var pug = require('gulp-pug');
var watch = require('gulp-watch');
var livereload = require('gulp-livereload');
var stylus = require('gulp-stylus');

gulp.task('html', function(){
  return gulp.src('app/templates/*pug')
  .pipe(pug({pretty: true}))
  .pipe(gulp.dest('app/templates/'));
  // .pipe(livereload());
});

gulp.task('css', function(){
  return gulp.src('app/static/css/*styl')
  .pipe(stylus())
  .pipe(gulp.dest('app/static/css/'));
  // .pipe(livereload());
});

gulp.task('watch', function() {
  gulp.watch('app/templates/*.pug', gulp.series('html'));
  gulp.watch('app/static/css/*.styl', gulp.series('css'));
});



//
// gulp.task('watch', function() {
//   // return watch('app/templates/*pug', {ignoreInitial: false})
//   //   .pipe(gulp.dest('pug'));
//   livereload.listen();
//   gulp.watch('app/templates/*.pug', ['html']);
// });

// gulp.task('default', ['watch']);
