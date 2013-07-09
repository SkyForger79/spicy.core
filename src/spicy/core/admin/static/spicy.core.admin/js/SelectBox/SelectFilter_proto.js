/*
SelectFilter2 - Turns a multiple-select box into a filter interface.

Different than SelectFilter because this is coupled to the admin framework.

Requires core.js, SelectBox.js and addevent.js.
*/

function findForm(node) {
    // returns the node of the form containing the given node
    if (node.tagName.toLowerCase() != 'form') {
        return findForm(node.parentNode);
    }
    return node;
}

var SelectFilter = {
    init: function(field_id, field_name, is_stacked, admin_media_prefix) {
        var from_box = $(field_id);
        from_box.id += '_from'; // change its ID
        from_box.className = 'filtered';

        // Remove <p class="info">, because it just gets in the way.
        var ps = from_box.parentNode.getElementsByTagName('p');
        for (var i=0; i<ps.length; i++) {
            from_box.parentNode.removeChild(ps[i]);
        }

        // <div class="selector"> or <div class="selector stacked">
        var selector_div = new Element('div',{'class':(is_stacked ? 'selector stacked' : 'selector')});
	from_box.parentNode.insert(selector_div);

        // <div class="selector-available">

        var selector_available = new Element('div',{'class':'selector-available'});
	selector_div.insert(selector_available);

        //quickElement('h2', selector_available, interpolate(gettext('Available %s'), [field_name]));
        var h2 = new Element('h2');
	selector_available.insert(h2);
	h2.update(interpolate(gettext('Available %s'), [field_name]));
	
	var filter_p = new Element('p',{'class':'selector-filter'});
	selector_available.insert(filter_p);

	var filter_ps = new Element('span',{'class':'ui-icon custom_ui-icon ui-icon-search-2'});
	filter_p.insert(filter_ps);
	filter_p.appendChild(document.createTextNode(' '));

	var filter_input = new Element('input',{'type':'text','id':field_id + '_input'});
	filter_p.insert(filter_input);
        selector_available.appendChild(from_box);

	var choose_all = new Element('a',{'class':'selector-chooseall','href':'javascript: (function(){ SelectBox.move_all("' + field_id + '_from", "' + field_id + '_to"); })()'});
	selector_available.insert(choose_all);choose_all.update(gettext('Choose all'));

        // <div class="selector-chooser">
	var selector_chooser = new Element('div',{'class':'selector-chooser'});
	selector_div.insert(selector_chooser);



	var add_link = new Element('a',{'class':'ui-corner-all custom_ui-icon icon','href':'javascript: (function(){ SelectBox.move("' + field_id + '_from","' + field_id + '_to");})()'});
	selector_chooser.insert(add_link);add_link.update("<i class='ui-icon custom_ui-icon ui-icon-arrow-2-e'>"+gettext('Add')+"</i>");

	var remove_link = new Element('a',{'class':'ui-corner-all icon','href':'javascript: (function(){ SelectBox.move("' + field_id + '_to","' + field_id + '_from");})()'});
	selector_chooser.insert(remove_link);remove_link.update("<i class='ui-icon custom_ui-icon  ui-icon-arrow-2-w'>"+gettext('Remove')+"</i>");

        // <div class="selector-chosen">
	var selector_chosen = new Element('div',{'class':'selector-chosen'});
	selector_div.insert(selector_chosen);     
	var h22 = new Element('h2',{'class':'selector-chosen'});
	selector_chosen.insert(h22);h22.update(interpolate(gettext('Chosen %s'), [field_name]));
        //var selector_filter = quickElement('p', selector_chosen, gettext('Select your choice(s) and click '));
        //selector_filter.className = 'selector-filter';
        //quickElement('img', selector_filter, '', 'src', admin_media_prefix + (is_stacked ? 'img/admin/selector_stacked-add.gif':'img/admin/selector-add.gif'), 'alt', 'Add');

	var to_box = new Element('select',{'id':field_id + '_to', 'multiple':'multiple', 'size':from_box.size, 'name': from_box.getAttribute('name'),'class':'filtered'
	});
	selector_chosen.insert(to_box); 


	var clear_all = new Element('a',{'class':'selector-clearall','href':'javascript: (function() { SelectBox.move_all("' + field_id + '_to", "' + field_id + '_from");})()'});
	selector_chosen.insert(clear_all); clear_all.update(gettext('Clear all'));

        from_box.setAttribute('name', from_box.getAttribute('name') + '_old');

        // Set up the JavaScript event handlers for the select box filter interface
        filter_input.observe('keyup', function(e) { SelectFilter.filter_key_up(e, field_id); });
        filter_input.observe( 'keydown', function(e) { SelectFilter.filter_key_down(e, field_id); });
        from_box.observe('dblclick', function() { SelectBox.move(field_id + '_from', field_id + '_to'); });
        to_box.observe('dblclick', function() { SelectBox.move(field_id + '_to', field_id + '_from'); });
        findForm(from_box).observe('submit', function() { SelectBox.select_all(field_id + '_to'); });
        SelectBox.init(field_id + '_from');
        SelectBox.init(field_id + '_to');
        // Move selected from_box options to to_box
        SelectBox.move(field_id + '_from', field_id + '_to');
    },
    filter_key_up: function(event, field_id) {
        from = $(field_id + '_from');
        // don't submit form if user pressed Enter
        if ((event.which && event.which == 13) || (event.keyCode && event.keyCode == 13)) {
            from.selectedIndex = 0;
            SelectBox.move(field_id + '_from', field_id + '_to');
            from.selectedIndex = 0;
            return false;
        }
        var temp = from.selectedIndex;
        SelectBox.filter(field_id + '_from', $(field_id + '_input').value);
        from.selectedIndex = temp;
        return true;
    },
    filter_key_down: function(event, field_id) {
        from = $(field_id + '_from');
        // right arrow -- move across
        if ((event.which && event.which == 39) || (event.keyCode && event.keyCode == 39)) {
            var old_index = from.selectedIndex;
            SelectBox.move(field_id + '_from', field_id + '_to');
            from.selectedIndex = (old_index == from.length) ? from.length - 1 : old_index;
            return false;
        }
        // down arrow -- wrap around
        if ((event.which && event.which == 40) || (event.keyCode && event.keyCode == 40)) {
            from.selectedIndex = (from.length == from.selectedIndex + 1) ? 0 : from.selectedIndex + 1;
        }
        // up arrow -- wrap around
        if ((event.which && event.which == 38) || (event.keyCode && event.keyCode == 38)) {
            from.selectedIndex = (from.selectedIndex == 0) ? from.length - 1 : from.selectedIndex - 1;
        }
        return true;
    }
}
