setTimeout(function () {
	var alert = document.getElementById("myAlert");
	if (alert) {
		alert.remove();
	}
}, 6000);

$(function () {
	$('[data-toggle="tooltip"]').tooltip()
  })

$(".plus-cart").click(function () {
	var id = $(this).attr("pid").toString();
	var qtyObj = this.parentNode.children[2];
	$.ajax({
		type: "GET",
		url: "/pluscart",
		data: {
			prod_id: id
		},
		success: function (data) {
			qtyObj.innerText = data.quantity;
			document.getElementById("amount").innerText = parseFloat(data.amount).toFixed(1);
			document.getElementById("totalamount").innerText = parseFloat(data.totalamount).toFixed(1);
		}
	});
});

$(".minus-cart").click(function () {
	var id = $(this).attr("pid").toString();
	var qtyObj = this.parentNode.children[2];
	$.ajax({
		type: "GET",
		url: "/minuscart",
		data: {
			prod_id: id
		},
		success: function (data) {
			qtyObj.innerText = data.quantity;
			document.getElementById("amount").innerText = data.amount;
			document.getElementById("totalamount").innerText = data.totalamount;
		}
	});
});

$(".remove-cart").click(function () {
	var id = $(this).attr("pid").toString();
	var qtyObj = this;
	$.ajax({
		type: "GET",
		url: "/removecart",
		data: {
			prod_id: id
		},
		success: function (data) {
			document.getElementById("amount").innerText = data.amount;
			document.getElementById("totalamount").innerText = data.totalamount;
			qtyObj.parentNode.parentNode.parentNode.parentNode.remove();
		}
	});
});

$('.plus-wishlist').click(function () {
	var id = $(this).attr("pid").toString();
	$(this).addClass('btn-danger');
	$(this).removeClass('btn-success');
	$.ajax({
		type: "GET",
		url: "/pluswishlist",
		data: {
			prod_id: id
		},
		success: function(data) {
			// alert(data.message)
			// window.location.href = `http://localhost:8000/product-detail/${id}`
			location.reload();
		}
	})
})

$('.minus-wishlist').click(function () {
	var id = $(this).attr("pid").toString();
	$(this).addClass('btn-success');
	$(this).removeClass('btn-danger');
	$.ajax({
		type: "GET",
		url: "/minuswishlist",
		data: {
			prod_id: id
		},
		success:function (data) {
			// alert(data.message)
			// window.location.href = `http://localhost:8000/product-detail/${id}`
			location.reload();
		}
	})
})
