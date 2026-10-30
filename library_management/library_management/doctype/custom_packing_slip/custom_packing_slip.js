frappe.ui.form.on("Custom Packing Slip", {
    setup(frm) {
        // Show only submitted Delivery Notes
        frm.set_query("custom_delivery_note", function () {
            return {
                filters: {
                    docstatus: 1
                }
            };
        });
    },

    custom_delivery_note(frm) {
        // Clear old rows when the Delivery Note changes
        frm.clear_table("custom_items");
        frm.refresh_field("custom_items");

        if (!frm.doc.custom_delivery_note) {
            return;
        }

        // Call our Python method
        frappe.call({
            method: "library_management.library_management.doctype.custom_packing_slip.custom_packing_slip.get_delivery_note_items",

            args: {
                delivery_note: frm.doc.custom_delivery_note
            },

            callback: function (r) {
                if (!r.message) {
                    return;
                }

                // Create destination rows from the returned data
                r.message.forEach(item => {
                    const row = frm.add_child("custom_items");

                    row.custom_item_code = item.item_code;
                    row.custom_item_name = item.item_name;
                    row.custom_batch_no = item.batch_no;
                    row.custom_description = item.description;
                    row.custom_qty = item.qty;
                    row.custom_net_weight = item.total_weight;
                    row.custom_stock_uom = item.stock_uom;
                    row.custom_weight_uom = item.weight_uom;
                    row.custom_page_break = item.page_break;
                    row.custom_dn_detail = item.dn_detail;
                });

                frm.refresh_field("custom_items");
            },

            error: function (error) {
                console.error(error);
                frappe.msgprint(
                    __("Unable to fetch the Delivery Note items.")
                );
            }
        });
    }
});