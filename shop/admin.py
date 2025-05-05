from django.contrib import admin
from .models import Category, Product, ProductReview
from django.utils.html import mark_safe
from .models import BroadcastMessage

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image_tag', 'description', 'price', 'discount_price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available', 'discount_price']
    prepopulated_fields = {'slug': ('name',)}

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'''
                    <style>
                        .modal-img {{
                            display: none;
                            position: fixed;
                            z-index: 9999;
                            padding-top: 50px;
                            left: 0;
                            top: 0;
                            width: 100%;
                            height: 100%;
                            background-color: rgba(0,0,0,0.9);
                        }}
                        .modal-img-content {{
                            margin: auto;
                            display: block;
                            max-width: 90%;
                            max-height: 90%;
                            border: 4px solid white;
                            box-shadow: 0 0 20px #000;
                        }}
                        .close-btn {{
                            position: absolute;
                            top: 20px;
                            right: 40px;
                            color: white;
                            font-size: 40px;
                            font-weight: bold;
                            cursor: pointer;
                            z-index: 10000;
                        }}
                    </style>
                    <img src="{obj.image.url}" width="100" height="100" style="cursor:pointer;border:1px solid #ccc" onclick="document.getElementById('modal-img-{obj.id}').style.display='block'"/>
                    <div id="modal-img-{obj.id}" class="modal-img">
                        <span class="close-btn" onclick="document.getElementById('modal-img-{obj.id}').style.display='none'">&times;</span>
                        <img class="modal-img-content" src="{obj.image.url}">
                    </div>
                ''')
        return '—'

    image_tag.short_description = 'Image'

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview)



@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(admin.ModelAdmin):
    list_display = ('short_message', 'active', 'created_at')
    list_editable = ('active',)
    list_filter = ('active', 'created_at')
    search_fields = ('message',)

    def short_message(self, obj):
        return f"{obj.message[:30]}..." if len(obj.message) > 30 else obj.message


