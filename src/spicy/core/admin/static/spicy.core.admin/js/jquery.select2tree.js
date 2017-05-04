(function($) {
    $.fn.select2tree = function(options, field_id) {
        var defaults = {
            language: "en",
            theme: "bootstrap",
        };
        var opts = $.extend(defaults, options);
        opts.templateResult = function(data, container) {
            if(data.element) {
                //insert span element and add 'parent' property
                var $wrapper = $("<span></span><span>" + data.text + "</span>");
                var $element = $(data.element);
                $(container).attr("val", $element.val());
                if($element.attr("parent")) {
                    $(container).attr("parent", $element.attr("parent"));
                }
                return $wrapper;
            } else {
                return data.text;
            }
        };
        $(this).select2(opts).on("select2:open", open);
    };
    function recursiveParentSelection(child, parentVals){
        var parentVal = child.attr('parent');
        var parent = $('li[val=' + parentVal + ']');
        parentVals.push(parentVal);
        if (parent.attr('parent') != undefined) { recursiveParentSelection(parent, parentVals); }
        else { $(field_id).val(parentVals).trigger('select2:select'); }
    }
    function getExistedValues(){
        var vals = [];
        $(field_id + ' option').each(function(){
            var optionText = $(this).text();
            var optVal = $(this).val();
            $('.select2-selection__choice').each(function(){
                if ($(this).text().replace('×', '') == optionText) {
                    vals.push(optVal);
                }
            });
        });
        return vals;
    }
    function selectTree(evt){
        var $this = $(this);
        var parentVals = getExistedValues();
        recursiveParentSelection($this, parentVals);
    }
    function moveOption(id) {
        if(id) {
            $(".select2-results__options li[parent=" + id + "]").insertAfter(".select2-results__options li[val=" + id + "]");
            $(".select2-results__options li[parent=" + id + "]").each(function() {
                moveOption($(this).attr("val"));
            });
        } else {
            $(".select2-results__options li:not([parent])").appendTo(".select2-results__options ul");
            $(".select2-results__options li:not([parent])").each(function() {
                moveOption($(this).attr("val"));
            });
        }
    }
    //deal switch action
    function switchAction(id, open) {
        $(".select2-results__options li[parent='" + id + "']").each(function() {
            switchAction($(this).attr("val"), open);
        });
        if(open) {
            $(".select2-results__options li[val=" + id + "] span[class]:eq(0)").removeClass("glyphicon-chevron-right").addClass("glyphicon-chevron-down");
            $(".select2-results__options li[parent='" + id + "']").slideDown();
        } else {
            $(".select2-results__options li[val=" + id + "] span[class]:eq(0)").addClass("glyphicon-chevron-right").removeClass("glyphicon-chevron-down");
            $(".select2-results__options li[parent='" + id + "']").slideUp();
        }
    }
    //get the level of li
    function getLevel(id) {
        var level = 0;
        while($(".select2-results__options li[parent][val='" + id + "']").length > 0) {
            id = $(".select2-results__options li[val='" + id + "']").attr("parent");
            level++;
        }
        return level;
    }
    function open() {
        setTimeout(function() {
            moveOption();
            $(".select2-results__options li").each(function() {
                var $this = $(this);
                //loop li add some classes and properties
                if($this.attr("parent")) {

                    $(this).siblings("li[val=" + $this.attr("parent") + "]").find("span:eq(0)").addClass("glyphicon glyphicon-chevron-down switch").css({
                        "cursor": "default"
                    });

                    $(this).siblings("li[val=" + $this.attr("parent") + "]").find("span:eq(1)").css("font-weight", "bold");
                }
                //add gap for children
                if(!$this.attr("style")) {
                    var paddingLeft = getLevel($this.attr("val")) * 2;
                    $("li[parent='" + $this.attr("parent") + "']").css("padding-left", paddingLeft + "em");
                }
                $this.on('mouseup', selectTree);
            });
        }, 0);
    }
})(jQuery);

