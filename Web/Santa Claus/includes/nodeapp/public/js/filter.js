function clean(s) {
	if (s === null) {
		return s;
	}
	return s
		.replace(
			/\/?script|img|svg|onload|onerror|alert|iframe|<|>|javascript|\[|\]|alert|document|cookie|location/gim,
			""
		)
		.replace(/\//gim, "\\/")
		.replace(/\\/gim, "\\");
}
