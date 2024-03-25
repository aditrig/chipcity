def join_table():
    document.getElementById('id_join_table').addEventListener('click', function() {
        window.location.href = '{%url 'table' %}}';
    })