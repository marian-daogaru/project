var gulp = require('gulp');
var pug = require('gulp-pug');

gulp.task('html', function(){
  return gulp.src('app/templates/*pug')
  .pipe(pug())
  .pipe(gulp.dest('app/templates'))
});

gulp.task('default', ['html']);
