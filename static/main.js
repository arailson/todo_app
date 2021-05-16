const montNames = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

$('#standard_calendar').calendar({
        type: 'date',
        today: true,
        monthFirst: false,
        text: {
            days: ['D', 'S', 'T', 'Q', 'Q', 'S', 'S'],
            months: montNames,
            monthsShort: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],
            today: 'Hoje'
        },
        formatter: {
            date: function (date, settings) {
                if (!date) return '';
                var day = date.getDate();
                var month = montNames[date.getMonth()];
                var year = date.getFullYear();
                return `${day} de ${month} de ${year}`
            }
        },
        onSelect: function(date,mode) {
            document.querySelector('#todo_date').value = date.toISOString().split('T')[0];
            return true;
        }
});
