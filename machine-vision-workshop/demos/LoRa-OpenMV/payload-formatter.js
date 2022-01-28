function decodeUplink(input) {
    var result = "";
    for (var i = 0; i < input.bytes.length; i++) {
        result += String.fromCharCode(parseInt(input.bytes[i]));
    }

    return {
        data: {
            bytes: input.bytes,
            message: result
        },
        warnings: [],
        errors: []
    };
}