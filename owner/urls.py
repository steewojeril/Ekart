from django.urls import path
from owner import views
urlpatterns=[
    path('index',views.AdminDashboard.as_view(),name='dashboard'),
    path('delivered',views.DeliveredView.as_view(),name='delivered'),
    path('recent_orders',views.RecentOrders.as_view(),name='recent_orders'),
    path('dispatched',views.DispatchedView.as_view(),name='dispatched'),
    path('in_transited',views.IntransitView.as_view(),name='intransited'),
    path('ordersdetail/<int:id>',views.OrderDetailView.as_view(),name='order-detail'),
    path('products',views.ProductsListView.as_view(),name='product_list'),
    path('products/<int:id>',views.ProductDetailView.as_view(),name='product_detail'),
    path('categories/add',views.CategoryAddView.as_view(),name='category_add'),
    path('categories/list',views.CategorysListView.as_view(),name='category_list'),
    path('categories/<int:id>/products',views.Category_ProductsListView.as_view(),name='category_products'),
    path('categories/<int:id>/products/add',views.AddProductView.as_view(),name='add_product'),
]