module.exports = function(grunt) {

  'use strict';

  var path = require('path');

  // Project configuration.
  grunt.log.writeln('srcBase: ' + grunt.option('srcBase'));
  var srcPath = path.normalize(grunt.option('srcBase') || 'website');
  grunt.log.writeln('srcPath: ' + srcPath);

  grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        project: {
            src: srcPath,
            images: '<%= project.src %>/images',
            cssDir: '<%= project.src %>/css',
            cssFile: '<%= project.cssDir %>/application.css',
            scss: '<%= project.cssDir %>/scss',
            js: '<%= project.src %>/scripts',
            html: '<%= project.src %>/views',
            bundles: '<%= project.js %>/bundles'
        },
        uglify: {
            options: {
                sourceMap: true,
                sourceMapIncludeSources: true,
                mangle: false
            }
        },
        useminPrepare: {
            html: ['<%= project.html %>/**/*.html', '<%= project.html %>/**/*.cshtml'],
            options: {
                root: '<%= project.src %>',
                dest: '<%= project.src %>',
                flow: {
                    steps: {
                        js: ['uglifyjs'],
                        css: ['concat', 'cssmin'] },
                    post: {}
                }
            }
        },
        usemin: {
            html: ['<%= project.html %>/**/*.html', '<%= project.html %>/**/*.cshtml'],
            options: {
                patterns: {
                    html: [
                        [/<script.+src=['"]([^"']+)["']/gm, 'Update the HTML to reference concat/min/revved script files']
                    ]
                },
                blockReplacements: {
                    js: function (block) {
                        return '<script src="' + block.dest + '?v=' + grunt.config('asset_cachebuster').options.buster + '"></script>';
                    }
                }
            }
        },
        asset_cachebuster: {
            options: {
                buster: Date.now(),
                ignore: ['http://', 'https://', '//', 'jquery', 'debugger', 'modernizr.2.6.2'],
                htmlExtension: 'cshtml'
            },
            build: {
                files: {
                  '<%= project.html %>/shared/layout/layout.cshtml': ['<%= project.html %>/shared/layout/layout.cshtml'],
                  '<%= project.html %>/app/index.cshtml': ['<%= project.html %>/app/index.cshtml'],
                  '<%= project.cssFile %>': '<%= project.cssFile %>',
                  '<%= project.cssDir %>/primer.css': '<%= project.cssDir %>/primer.css'
                }
            }
        },
        autoprefixer: {
            primer: {
                files: {
                    '<%= project.cssDir %>/primer.css': '<%= project.cssDir %>/primer.css'
                },
                options: {
                    map: true
                }
            },
            application: {
                files: {
                    '<%= project.cssFile %>': '<%= project.cssFile %>'
                },
                options: {
                    map: true
                }
            }
        },
        imagemin: {
            dynamic: {
                files: [{
                    expand: true,
                    cwd: '<%= project.images %>/sprites',
                    src: ['*.{png,jpg,gif,svg}'],
                    dest: '/'
                }]
            }
        },
        sass: {
            release: {
                options: {
                    style: 'expanded'
                    //style: 'compressed'
                },
                files: {
                    '<%= project.cssDir %>/application.css': '<%= project.scss %>/application.scss',
                    '<%= project.cssDir %>/primer.css': '<%= project.scss %>/sw-primer/primer.scss'
                }
            }
        },
        sprite: {
            about: {
                src: '<%= project.images %>/sprites/about/*.png',
                destImg: '<%= project.images %>/sprites/sprite-about.png',
                destCSS: '<%= project.scss %>/sprites/_sprite-about.scss',
                cssVarMap: function (sprite) {
                    sprite.name = 'about-' + sprite.name;
                },
                algorithm: 'binary-tree'
            },
            home: {
                src: '<%= project.images %>/sprites/home/*.png',
                destImg: '<%= project.images %>/sprites/sprite-home.png',
                destCSS: '<%= project.scss %>/sprites/_sprite-home.scss',
                cssVarMap: function (sprite) {
                    sprite.name = 'home-' + sprite.name;
                },
                algorithm: 'binary-tree'
            },
            icon: {
                src: '<%= project.images %>/sprites/icon/*.png',
                destImg: '<%= project.images %>/sprites/sprite-icon.png',
                destCSS: '<%= project.scss %>/sprites/_sprite-icon.scss',
                cssVarMap: function (sprite) {
                    sprite.name = 'icon-' + sprite.name;
                },
                algorithm: 'binary-tree'
            },
            pricing: {
                src: '<%= project.images %>/sprites/pricing/*.png',
                destImg: '<%= project.images %>/sprites/sprite-pricing.png',
                destCSS: '<%= project.scss %>/sprites/_sprite-pricing.scss',
                cssVarMap: function (sprite) {
                    sprite.name = 'pricing-' + sprite.name;
                },
                algorithm: 'binary-tree'
            },
            clients: {
                src: '<%= project.images %>/sprites/client/*.png',
                destImg: '<%= project.images %>/sprites/sprite-client.png',
                destCSS: '<%= project.scss %>/sprites/_sprite-client.scss',
                cssVarMap: function (sprite) {
                    sprite.name = 'client-' + sprite.name;
                },
                algorithm: 'binary-tree'
            }
        },
        watch: {
            options: {
                spawn: false,
                livereload: true
            },
            scripts: {
                files: ['<%= project.js %>*//***/*//*.js']
            },
            css: {
                files: ['<%= project.scss %>/**/*.scss'],
                tasks: ['sass', 'autoprefixer']
            },
            sprites: {
                files: ['<%= project.images %>/sprites/**/*.png'],
                tasks: ['sprite']
            },
            html: {
                files: ['<%= project.html %>/**/*.cshtml']
            }
        }
    });

    // Load plugins
    grunt.loadNpmTasks('grunt-contrib-imagemin');
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-usemin');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-autoprefixer');
    grunt.loadNpmTasks('grunt-spritesmith');
    grunt.loadNpmTasks('grunt-asset-cachebuster');
    grunt.loadNpmTasks('grunt-contrib-concat');

    // Set Tasks
    grunt.registerTask('default', ['dev', 'watch']); // if the file has changes
    grunt.registerTask('dev', ['sass', 'autoprefixer']);
    grunt.registerTask('build', ['dev', 'useminPrepare', 'uglify', 'usemin', 'asset_cachebuster']);
};