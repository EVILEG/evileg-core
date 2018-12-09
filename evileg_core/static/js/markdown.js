let allEditors = {};
let selectionRange = null;

jQuery.fn.extend({
insertAtCaret: function(myValue){
  return this.each(function(i) {
    if (document.selection) {
      //For browsers like Internet Explorer
      this.focus();
      var sel = document.selection.createRange();
      sel.text = myValue;
      this.focus();
    }
    else if (this.selectionStart || this.selectionStart == '0') {
      //For browsers like Firefox and Webkit based
      var startPos = this.selectionStart;
      var endPos = this.selectionEnd;
      var scrollTop = this.scrollTop;
      this.value = this.value.substring(0, startPos)+myValue+this.value.substring(endPos,this.value.length);
      this.focus();
      this.selectionStart = startPos + myValue.length;
      this.selectionEnd = startPos + myValue.length;
      this.scrollTop = scrollTop;
    } else {
      this.value += myValue;
      this.focus();
    }
  });
}
});

class EMarkdownEditor {
    constructor (widgetId) {
        this.id = widgetId;
        this.textarea = jQuery("#" + widgetId);
        this.tabPreviewLink = jQuery("#" + widgetId + "_tab_preview_link");
        this.tabPreviewLink.bind('shown.bs.tab', {widgetId: widgetId}, EMarkdownEditor.updatePreview);
        // Link Dialog
        this.linkDialog = jQuery("#" + widgetId + "_add_link_dialog");
        this.addLinkBtn = jQuery("#" + widgetId + "_add_link_btn");
        this.addLinkBtn.bind('click', {dialog: this.linkDialog}, EMarkdownEditor.showDialog);
        this.insertLinkBtn = jQuery("#" + widgetId + "_insert_link_btn");
        this.insertLinkBtn.bind('click', {widgetId: widgetId}, EMarkdownEditor.insertLink);
        this.linkText = jQuery("#" + widgetId + "_link_text");
        this.linkUrl = jQuery("#" + widgetId + "_link_url");
        // Code Dialog
        this.codeDialog = jQuery("#" + widgetId + "_code_dialog");
        this.addCodeBtn = jQuery("#" + widgetId + "_add_code_btn");
        this.addCodeBtn.bind('click', {dialog: this.codeDialog}, EMarkdownEditor.showDialog );
        this.insertCodeBtn = jQuery("#" + widgetId + "_insert_code_btn");
        this.insertCodeBtn.bind('click', {widgetId: widgetId}, EMarkdownEditor.insertCode);
        this.selectCode = jQuery('#' + widgetId + '_select_code');
        this.codeInput = jQuery('#' + widgetId + '_code_input');
    }

    static insertCode(e) {
        e.preventDefault();
        let editor = EMarkdownEditor.get(e.data.widgetId);
        if (editor) {
            let code = editor.codeInput.val();
            let lang = editor.selectCode.val();
            if (code.length > 0)
            {
                let resultCode = '\n```' + lang + '\n' + code + '\n```\n';
                EMarkdownEditor.restoreSelection();
                editor.textarea.insertAtCaret(resultCode);
                editor.code_input.val('');
                return true;
            }
        }
        return false;
    }

    static insertLink(e) {
        e.preventDefault();
        let editor = EMarkdownEditor.get(e.data.widgetId);
        if (editor) {
            let linkUrl = editor.linkUrl.val();
            if (linkUrl.length > 0) {
                let linkText = editor.linkText.val();
                let link;
                if (linkText.length > 0) {
                    link = "[" + linkText + "](" + linkUrl + ")"
                }
                else {
                    link = "[" + linkUrl + "](" + linkUrl + ")"
                }
                EMarkdownEditor.restoreSelection();
                editor.textarea.insertAtCaret(link);
                editor.linkUrl.val('');
                editor.linkText.val('');
                return true;
            }
        }
        return false;
    }

    static showDialog(e) {
        e.data.dialog.modal('show');
        return false;
    }

    static create(widgetId) {
        let editor = new EMarkdownEditor(widgetId);
        allEditors[widgetId] = editor;
        return editor;
    }

    static remove(widgetId) {
        delete allEditors[widgetId];
    }

    static get(widgetId) {
        return allEditors[widgetId];
    }

    static saveSelection() {
        if (window.getSelection) {
            let sel = window.getSelection();
            if (sel.getRangeAt && sel.rangeCount) {
                return sel.getRangeAt(0);
            }
        } else if (document.selection && document.selection.createRange) {
            return document.selection.createRange();
        }
        return null;
    }

    static restoreSelection(range) {
        if (range) {
            if (window.getSelection) {
                let sel = window.getSelection();
                sel.removeAllRanges();
                sel.addRange(range);
            } else if (document.selection && range.select) {
                range.select();
            }
        }
    }

    static updatePreview(e) {
        let widgetId = e.data.widgetId;
        $.ajax({
            url: '/evileg_core/markdown/',
            type: 'POST',
            data: {'content': jQuery('#' + widgetId).val(),},
            dataType: 'json',

            success: function (json) {
                jQuery('#' + widgetId + '_preview').html(json.preview);
                prettyPrint();
            }
        });
    }
}