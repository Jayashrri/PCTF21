const userEmail = parseJwt(getCookie("jwt")).email;
if (userEmail !== "admin1337bs@beautifulsites.com") {
	document.getElementById("preview").innerText =
		"Your interviewer will view this page before calling for interview.";
	document.getElementById("userSubmit").removeAttribute("hidden");
} else {
	document.getElementById("adminOptions").removeAttribute("hidden");
}
let currentYear = String(new Date().getFullYear());
const urlParams = new URLSearchParams(window.location.search);
document.getElementById("name").innerText = clean(urlParams.get("name"));
document.getElementById("nameform").value = clean(urlParams.get("name"));
document.getElementById("dob").innerText = clean(urlParams.get("dob"));
document.getElementById("dobform").value = clean(urlParams.get("dob"));
const cleanDate = clean(urlParams.get("dob"));
const year = cleanDate.split("-")[0];
const age = eval(`${currentYear} - ${year}`);
document.getElementById("age").innerText = age;
document.getElementById("education").innerText = urlParams.get("education");
document.getElementById("educationform").value = urlParams.get("education");
document.getElementById("job").innerText = urlParams.get("job");
document.getElementById("jobform").value = urlParams.get("job");

$("#jobAccept").click((e) => {
	e.preventDefault();
	const nameform = $("#nameform").val();
	const dobform = $("#dobform").val();
	const eduform = $("#educationform").val();
	const jobform = $("jobform").val();
	$.ajax({
		type: "POST",
		url: "/jobAccept",
		data: { nameform, dobform, eduform, jobform },
		dataType: "text",
		success: function (result) {
			if (JSON.parse(result).accept === "fail") {
				alert("Don't try to fool the server");
			} else {
				alert("Accepted Job");
			}
		},
	});
});

$("#jobReject").click((e) => {
	e.preventDefault();
	const nameform = $("#nameform").val();
	const dobform = $("#dobform").val();
	const eduform = $("#educationform").val();
	const jobform = $("jobform").val();
	$.ajax({
		type: "POST",
		url: "/jobReject",
		data: { nameform, dobform, eduform, jobform },
		dataType: "text",
		success: function (result) {
			if (JSON.parse(result).reject === "fail") {
				alert("Don't try to fool the server");
			} else {
				alert("Rejected Job");
			}
		},
	});
});
