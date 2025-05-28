
class Formatters {
    static formatNumber(value) {
        return parseFloat(value).toFixed(2);
    }

    static formatCurrency(value) {
        const amount = parseFloat(value).toFixed(2);
        if (isNaN(amount)) {
            return "0.00";
        }

        const formatter = new Intl.NumberFormat("en-GH", {
            style: "currency",
            currency: "GHS",
            currencyDisplay: "symbol",
        });
        return formatter.format(amount);
    }

    static formatDate(date) {
        const d = new Date(date);
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(
            2,
            "0"
        )}-${String(d.getDate()).padStart(2, "0")}`;
    }

    static formatTime(date) {
        const d = new Date(date);
        return `${String(d.getHours()).padStart(2, "0")}:${String(
            d.getMinutes()
        ).padStart(2, "0")}`;
    }

    static formatPaymentMethod(method) {
        const methods = {
            cash: "Cash",
            card: "Credit/Debit Card",
            bank_transfer: "Bank Transfer",
        };
        return methods[method] || method;
    }
};

export default Formatters;