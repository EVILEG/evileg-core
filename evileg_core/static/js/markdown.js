let allEditors = {};
let LANGUAGES = {
    "": "text/x-c++src",
    "lang-bsh": "text/x-sh",
    "lang-c": "text/x-csrc",
    "lang-cc": "text/x-csrc",
    "lang-cpp": "text/x-c++src",
    "lang-cs": "text/x-c++src",
    "lang-csh": "text/x-c++src",
    "lang-cyc": "text/x-c++src",
    "lang-cv": "text/x-c++src",
    "lang-htm": "text/html",
    "lang-html": "text/html",
    "lang-java": "text/x-java",
    "lang-js": "text/javascript",
    "lang-m": "text/html",
    "lang-mxml": "text/html",
    "lang-perl": "text/x-perl",
    "lang-pl": "text/x-sh",
    "lang-pm": "text/x-sh",
    "lang-py": "text/x-python",
    "lang-rb": "text/x-ruby",
    "lang-sh": "text/x-sh",
    "lang-xhtml": "htmlmixed",
    "lang-xml": "text/html",
    "lang-xsl": "text/html",
};

class EMarkdownEditor {
    constructor (widgetId, uploadLink='', uploadFileLink='') {
        let editor = this;
        this.fullscreen = false;
        this.id = widgetId;
        this.widget = jQuery('#' + widgetId + '_markdown_widget');
        this.textarea = jQuery("#" + widgetId);
        this.tabPreviewLink = jQuery("#" + widgetId + "_tab_preview_link");
        this.tabPreviewLink.bind('shown.bs.tab', {widgetId: widgetId}, EMarkdownEditor.updatePreview);
        // Fullscreen
        this.fullScreenButton = jQuery("#" + widgetId + "_fullscreen_btn");
        this.fullScreenButton.on('click', function(e){
            e.preventDefault();
            editor.fullScreen();
        });
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
        this.selectCode.bind('change', {widgetId: widgetId}, EMarkdownEditor.onSelectCode);
        this.codeInput = jQuery('#' + widgetId + '_code_input');
        // Upload Image Dialog
        this.uploadLink = uploadLink;
        this.addImageBtn = jQuery('#' + widgetId + '_add_image_btn');
        this.addImageBtn.bind("click", {widgetId: widgetId}, EMarkdownEditor.showUploadDialog);
        // Upload file dialog
        this.uploadFileLink = uploadFileLink;
        this.addFileBtn = jQuery('#' + widgetId + '_add_file_btn');
        this.addFileBtn.bind('click', {widgetId: widgetId}, EMarkdownEditor.showUploadFileDialog);
        // Add special symbols
        this.addCutBtn = jQuery('#' + widgetId + '_add_cut_btn');
        this.addCutBtn.bind('click', {widgetId: widgetId}, EMarkdownEditor.insertCut);

        // Code Mirror - Code Editor
        try {
            this.mirrorEditor = eval(widgetId + '_code_input_codemirror');
            this.mirrorEditor.on('change', function (cm) {
                editor.codeInput.val(cm.getValue());
            });
            this.mirrorEditor.setOption("extraKeys", {
                "Ctrl-/": "toggleComment"
            });
        }
        catch(err) {
            console.log("Code editor not found");
        }

        // Code Mirror - Markdown Editor
        try {
            this.markdownMirrorEditor = eval(widgetId + '_codemirror');
            this.markdownMirrorEditor.on('change', function (cm) {
                editor.textarea.val(cm.getValue());
            });

            this.markdownMirrorEditor.setOption("extraKeys", {
                "F11": function (cm) {
                    editor.fullScreen();
                },
                "Esc": function (cm) {
                    editor.widget.removeClass('markdown-fullscreen');
                    editor.fullscreen = false;
                    editor.fullScreenButton.find('span').removeClass('mdi-fullscreen-exit');
                    editor.fullScreenButton.find('span').addClass('mdi-fullscreen');
                },
                "Ctrl-/": "toggleComment"
            });
        }
        catch (err) {
            console.log("Markdown editor not found");
        }
    }

    fullScreen() {
        if (this.fullscreen) {
            this.widget.removeClass('markdown-fullscreen');
            this.fullscreen = false;
            this.fullScreenButton.find('span').removeClass('mdi-fullscreen-exit');
            this.fullScreenButton.find('span').addClass('mdi-fullscreen');
        } else {
            this.widget.addClass('markdown-fullscreen');
            this.fullscreen = true;
            this.fullScreenButton.find('span').removeClass('mdi-fullscreen');
            this.fullScreenButton.find('span').addClass('mdi-fullscreen-exit');
        }
    }

    static onSelectCode(e) {
        let editor = EMarkdownEditor.get(e.data.widgetId);
        editor.mirrorEditor.setOption("mode", LANGUAGES[editor.selectCode.val()])
    }

    static insertCut(e) {
        e.preventDefault();
        let editor = EMarkdownEditor.get(e.data.widgetId);
        if (editor) {
            editor.markdownMirrorEditor.replaceSelection('\n___\n');
        }
        return false;
    }

    static showUploadDialog(e) {
        e.preventDefault();
        let widgetId = e.data.widgetId;
        let editor = EMarkdownEditor.get(widgetId);
        if (editor.uploadLink.length) {
            let uploadDialog = jQuery('#uploadDialog');
            if (uploadDialog.length) {
                EMarkdownEditor.initUploadDialog(widgetId);
                uploadDialog.modal('show');
            } else {
                jQuery.ajax({
                    url: editor.uploadLink,
                    type: 'GET',
                    dataType: 'json',

                    success: function (json) {
                        jQuery(json.uploadDialog).appendTo(jQuery('body'));
                        EMarkdownEditor.showUploadDialog(e);
                    }
                });
            }
        }
    }

    static initUploadDialog(widgetId) {
        let editor = EMarkdownEditor.get(widgetId);
        let uploadDialog = jQuery('#uploadDialog');
        uploadDialog.find("#id_file").change(function () {
            if (this.files && this.files[0]) {
                let reader = new FileReader();
                reader.onload = function (e) {
                    let img = jQuery("#upload_image");
                    img.on("load", function (e) {
                        let cropper = new Cropper(upload_image, { viewMode: 1 });
                        uploadDialog.find("#js-zoom-in").click(function () { cropper.zoom(0.1); });
                        uploadDialog.find("#js-zoom-out").click(function () { cropper.zoom(-0.1); });
                        uploadDialog.on("hidden.bs.modal", function () {
                            cropper.destroy();
                        });

                        uploadDialog.find("#js-crop-and-upload").click(function (e) {
                            e.preventDefault();
                            let formUpload = new FormData(uploadDialog.find("#formUpload").get(0));
                            if (formUpload) {

                                let canvas = cropper.getCroppedCanvas();
                                canvas.toBlob(function (blob) {
                                    formUpload.set('file', blob, 'photo.jpg');

                                    jQuery.ajax({
                                        url: editor.uploadLink,
                                        type: "POST",
                                        data: formUpload,
                                        cache: false,
                                        processData: false,
                                        contentType: false,
                                        success: function (json) {
                                            if (json.result) {
                                                let image = '\n[![' + json.description + '](' + json.src + ')](' + json.url + ')\n';
                                                editor.markdownMirrorEditor.replaceSelection(image);
                                                uploadDialog.find("#upload-size-warning").addClass("d-none");
                                                uploadDialog.modal("hide");
                                            }
                                        },
                                        error: function (jqXHR, textStatus, errorThrown) {
                                            if (jqXHR.status === 413) {
                                                uploadDialog.find("#upload-size-warning").removeClass("d-none");
                                            }
                                        }
                                    });
                                });
                            }
                            return false;
                        });

                        uploadDialog.find("#upload-size-warning").addClass("d-none");
                        uploadDialog.find("#cropBody").removeClass("d-none");
                        uploadDialog.find("#cropFooter").removeClass("d-none");
                        uploadDialog.find("#file_form_group").addClass("d-none");
                        uploadDialog.find("#id_content").parent().removeClass("d-none");
                    });
                    img.attr("src", e.target.result);
                };
                reader.readAsDataURL(this.files[0]);
            }
        });

        uploadDialog.on("hidden.bs.modal", function () {
            uploadDialog.remove();
        });
    }

    static  initUploadFileDialog(widgetId) {
        let editor = EMarkdownEditor.get(widgetId);
        let uploadFileDialog = jQuery('#uploadFileDialog');
        uploadFileDialog.find("#id_file").change(function (e) {
            if (this.files && this.files[0]) {
                uploadFileDialog.find('#file-upload-submit').click(function (e) {
                    e.preventDefault();
                    let formUpload = new FormData(uploadFileDialog.find("#formUpload").get(0));
                    if (formUpload) {
                        jQuery.ajax({
                            url: editor.uploadFileLink,
                            type: "POST",
                            data: formUpload,
                            cache: false,
                            processData: false,
                            contentType: false,
                            success: function (json) {
                                if (json.result) {
                                    let file = '\n[![' + json.name + '](/static/images/file.svg) ' + json.name + '](' + json.url + ')\n';
                                    editor.markdownMirrorEditor.replaceSelection(file);
                                    uploadFileDialog.find("#upload-size-warning").addClass("d-none");
                                    uploadFileDialog.modal("hide");
                                }
                            },
                            error: function (jqXHR, textStatus, errorThrown) {
                                if (jqXHR.status === 413) {
                                    uploadFileDialog.find("#upload-size-warning").removeClass("d-none");
                                }
                            }
                        });
                    }
                    return false;
                });

                uploadFileDialog.find("#file_info").removeClass("d-none");
                uploadFileDialog.find("#file_name").html(e.target.files[0].name);
                uploadFileDialog.find("#file_form_group").addClass("d-none");
                uploadFileDialog.find("#id_content").parent().removeClass("d-none");
                uploadFileDialog.find(("#uploadFooter")).removeClass("d-none");
            }
        });

        uploadFileDialog.on("hidden.bs.modal", function () {
            uploadFileDialog.remove();
        });
    }

    static showUploadFileDialog(e) {
        e.preventDefault();
        let widgetId = e.data.widgetId;
        let editor = EMarkdownEditor.get(widgetId);
        if (editor.uploadFileLink.length) {
            let uploadDialog = jQuery('#uploadFileDialog');
            if (uploadDialog.length) {
                EMarkdownEditor.initUploadFileDialog(widgetId);
                uploadDialog.modal('show');
            } else {
                jQuery.ajax({
                    url: editor.uploadFileLink,
                    type: 'GET',
                    dataType: 'json',

                    success: function (json) {
                        jQuery(json.uploadDialog).appendTo(jQuery('body'));
                        EMarkdownEditor.showUploadFileDialog(e);
                    }
                });
            }
        }
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
                editor.markdownMirrorEditor.replaceSelection(resultCode);
                editor.codeInput.val('');
                editor.mirrorEditor.getDoc().setValue('');
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
                editor.markdownMirrorEditor.replaceSelection(link);
                editor.linkUrl.val('');
                editor.linkText.val('');
                return true;
            }
        }
        return false;
    }

    static showDialog(e) {
        e.data.dialog.modal('show');
        e.data.dialog.css('z-index', 2000);
        return false;
    }

    static create(widgetId, upload_link='', upload_file_link) {
        let editor = new EMarkdownEditor(widgetId, upload_link, upload_file_link);
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