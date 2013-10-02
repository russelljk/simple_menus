(function($){
	function NestedList(el, options) {

		//Defaults:
		this.defaults = {
            MAX_LEVELS: 2,
            INDENT_LEVEL: 20,
            LIST_MARGIN_SIZE: 5,
            onStop: undefined
		};
        
		//Extending options:
		this.opts = $.extend({}, this.defaults, options);
    
		//Privates:
		this.$el = $(el);
	}
    
	// Separate functionality from object creation
	NestedList.prototype = {            
		init: function() {
			var _this = this;
            _this.initSorting();            
		},
        initSorting: function() {
            var currentDepth = 0;
            var originalDepth = 0;
            var itemChildren = null;
            var childrenDepth = 0;
            var _this = this;
            var hasChanged = false;
            var sortListEdge = _this.$el.offset().left;
            
            var makeDepth = function(left) {
                var depth = Math.floor(left/_this.opts.INDENT_LEVEL);
                return Math.max(0, Math.min(depth, _this.opts.MAX_LEVELS));
            };
            
            var itemDepth = function(item) {
                var ml = parseInt(item.css('margin-left'));
                return makeDepth(ml);
            };  
    
            var setDepth = function(item, d) {
                currentDepth = d;
                updateDepth(item);
            };
            
            var updateDepth = function(item) {
                for (var d = 0; d <= _this.opts.MAX_LEVELS; ++d) {
                    if (d != currentDepth) {
                        item.removeClass('level-'+d);
                    }
                }
                var offset = currentDepth - originalDepth;
                //$foo.html(offset);
                var depth_class = 'level-'+currentDepth;
                item.addClass(depth_class);
                item.attr('data-level', currentDepth);
            };
            
            //var $sortables = $('#sortable');
            
            var findChildren = function(item) {
                var next = item.next();
                var depth = itemDepth(item);
                var items = $();
                while (next.length) {
                    var next_depth = itemDepth(next);
                    if (next_depth <= depth) {
                        break;
                    } else {
                        childrenDepth = Math.max(childrenDepth, next_depth);
                        items = items.add(next);
                    }
                    next = next.next();
                }            
                return items;
            };
            
            var checkDepth = function(prev_depth, depth, next_depth) {
                if (next_depth > prev_depth) {
                    return next_depth;
                } 
                else if (depth >= prev_depth + 1) {
                    return prev_depth + 1;
                } else if (next_depth == prev_depth) {
                    return prev_depth;
                }
                return depth;
            };
            
    		_this.$el.sortable({
    			handle: 'div.handle',
    			items: 'li',
                placeholder: 'placeholder',
                delay: 150,
                distance: 5,
                forceHelperSize: true,
                sort: function(e, ui) {
                    // Find out the depth based on the horizontal position.                                        
                    var left =  ui.helper.offset().left - sortListEdge;//ui.helper.offset().left;
                    var depth = makeDepth(left);
                    
                    // We only care about updating if either the depth or index
                    // has changed since the last time.
                    if (!hasChanged) {
                        if (depth == currentDepth) {
                            return;
                        }
                    } else {
                        hasChanged = false; // So that we can skip the next update if its the same.
                    }
                    
                    var prev = ui.placeholder.prev(), next = ui.placeholder.next();
    				if( prev[0] == ui.item[0] ) prev = prev.prev();
    				if( next[0] == ui.item[0] ) next = next.next();
            
                    var prev_depth = null;
                    var next_depth = null;
            
                    if (prev.length) {
                        prev_depth = prev.attr('data-level'); prev_depth = parseInt(prev_depth);
                    }
                            
                    if (next.length) { next_depth = next.attr('data-level'); next_depth = parseInt(next_depth); }
                    
                    if (prev_depth === null) { 
                        depth = 0;
                    } else {
                        if (prev_depth <= depth) {
                            if (next_depth !== null) {                            
                                depth = checkDepth(prev_depth, depth, next_depth);
                            }
                            else if (depth > prev_depth + 1) {
                                depth = prev_depth + 1;
                            }
                        } else {
                            if (next_depth !== null) {
                                depth = checkDepth(prev_depth, depth, next_depth);
                            }
                        }
                    }     
            
                    if (currentDepth != depth) {
                        ui.placeholder.removeClass('level-'+currentDepth);
                
                        // Check to make sure any children will not have
                        // thier depth squashed.
                        if (childrenDepth) {
                            var offset = originalDepth - depth;
                            if (offset != 0) {
                                if ((childrenDepth - offset) > _this.opts.MAX_LEVELS) {                                
                                    depth = currentDepth;
                                }
                            }
                        }
                
                        var depth_class = 'level-'+depth;
                        ui.placeholder.addClass(depth_class);
                        currentDepth = depth;
                    }
                },
    			change: function(e, ui) {
                    
                    hasChanged = true;
                    var prev = ui.item.prev();
                    if( ! ui.placeholder.parent().hasClass('issortable') ) {
                        if (prev.length) {
                            prev.after( ui.placeholder );
                        } else {
                            _this.$el.prepend( ui.placeholder );
                        }
                    }
    			},
                start: function(e, ui) {
                    var transport, classes;
                    var item = ui.item.children('div');
                    
                    itemChildren = null;
                    transport = ui.item.children('.child-box');
			        
                    originalDepth = itemDepth(ui.item);
                    childrenDepth = 0;
                    setDepth(ui.placeholder, originalDepth);
                    var parent = ( ui.item.next()[0] == ui.placeholder[0] ) ? ui.item.next() : ui.item;
                    itemChildren = findChildren(parent);
    				
                    height = item.parent().outerHeight();
                    
                    if (itemChildren) {
                        transport.append(itemChildren);
                        height += transport.outerHeight();
                        if (itemChildren.length)                   
                            height += _this.opts.LIST_MARGIN_SIZE;
                    }                
                    
    				height -= 4; // Placeholder has 2px border
    				ui.placeholder.height(height);
                },
                stop: function(e, ui) {
                    if (originalDepth != currentDepth) {
                        if (itemChildren.length) {
                            var offset = originalDepth - currentDepth;
                            itemChildren.each(function(index) {
                                var item = $(itemChildren[index]);
                                var level = parseInt(item.attr('data-level'));
                                level -= offset;
                                level = Math.max(0, Math.min(level, _this.opts.MAX_LEVELS));
                                var oldDepth = currentDepth;
                                currentDepth = level;
                                updateDepth(item);
                                currentDepth = oldDepth;
                            });
                        }
                    } else {
                        
                    }
                    updateDepth(ui.item);
                    if (itemChildren.length) {
                        itemChildren.insertAfter(ui.item);
                    }
                    
                    if (_this.opts.onStop) {
                        _this.opts.onStop(ui.item);
                    }
                }
            });  
        }
	};
    
	// The actual plugin
	$.fn.nestedList = function(options) {
		if (this.length) {
			this.each(function() {
				var rev = new NestedList(this, options);
				rev.init();
				$(this).data('nestedList', rev);
			});
		}
	};
})(jQuery);
