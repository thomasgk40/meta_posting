// Copyright (c) 2024, Printechs and contributors
// For license information, please see license.txt

frappe.ui.form.on('Social Media Post', {
    post_now: function(frm) {
        frappe.call({
            method: "meta_posting.social_media_posting.doctype.social_media_post.social_media_post.post_to_social_media",
            args: { docname: frm.doc.name },
            callback: function(response) {
                if (response.message) {
                    frappe.msgprint(response.message);
                    frm.reload_doc();
                }
            }
        });
    }
});
