/*
http://ruseller.com/lessons.php?rub=32&id=999
*/

$.fn.stickyfloat = function(options, lockBottom) {
                var $obj                = this;
                var parentPaddingTop    = parseInt($obj.parent().css('padding-top'));
                var startOffset         = $obj.parent().offset().top;
                var opts                = $.extend({ startOffset: startOffset, offsetY: parentPaddingTop, duration: 10, lockBottom:true }, options);

                $obj.css({ position: 'absolute', 'z-index': 1000, width: '100%'});

                if(opts.lockBottom){
                    var bottomPos = $obj.parent().height() - $obj.height() + parentPaddingTop;
                    if( bottomPos < 0 )
                        bottomPos = 0;
                }

                $(window).scroll(function () {
                    $obj.stop();

                    var pastStartOffset         = $(document).scrollTop() > opts.startOffset;
                    var objFartherThanTopPos    = $obj.offset().top > startOffset;
                    var objBiggerThanWindow     = $obj.outerHeight() < $(window).height();

                    if( (pastStartOffset || objFartherThanTopPos) && objBiggerThanWindow ){
                        var newpos = ($(document).scrollTop() -startOffset + opts.offsetY );
			newpos += 30;
                        if ( newpos > bottomPos )
                            newpos = bottomPos;
                        if ( $(document).scrollTop() < opts.startOffset )
                            newpos = parentPaddingTop;

                        $obj.animate({ top: newpos }, opts.duration );
                    }
                });
            };

