var gulp = require('gulp');
var pug = require('gulp-pug');
var watch = require('gulp-watch');
var livereload = require('gulp-livereload');

gulp.task('html', function(){
  return gulp.src('app/templates/*pug')
  .pipe(pug({pretty: true}))
  .pipe(gulp.dest('app/templates/'));
  // .pipe(livereload());
});


gulp.task('watch', function() {
  gulp.watch('app/templates/*.pug', gulp.series('html'));
});



//
// gulp.task('watch', function() {
//   // return watch('app/templates/*pug', {ignoreInitial: false})
//   //   .pipe(gulp.dest('pug'));
//   livereload.listen();
//   gulp.watch('app/templates/*.pug', ['html']);
// });

// gulp.task('default', ['watch']);
