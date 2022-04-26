document.addEventListener('DOMContentLoaded', function () {
    const stadium = document.querySelectorAll('.stadium');
    const bonus_type = document.querySelector('#bonus_type');
    const quantity = document.querySelector('#quantity');
})


function create_form_bonus() {
    _html = `
    <div class="bonus">
        <h3>Olmecabono</h3>
        <p><span>fdgfdgd</span> <span>fdsdff</span></p>
        <div class="grid grid-cols-6 gap-6">
            <div class="col-span-6 sm:col-span-6">
                <label for="full_name">Nombre completo</label>
                <input type="text" name="full_name" id="full_name">
            </div>
            <div class="col-span-6 sm:col-span-3">
                <label for="phone_number">Teléfono</label>
                <input type="text" name="phone_number" id="phone_number">
            </div>
            <div class="col-span-6 sm:col-span-3">
                <label for="email">Correo electrónico</label>
                <input type="text" name="email" id="email">
            </div>
            <div class="col-span-6 sm:col-span-6 lg:col-span-2">
                <label for="section">Sección</label>
                <input type="text" name="section" id="section">
            </div>
            <div class="col-span-6 sm:col-span-3 lg:col-span-2">
                <label for="row">Fila</label>
                <input type="text" name="row" id="row">
            </div>
            <div class="col-span-6 sm:col-span-3 lg:col-span-2">
                <label for="seat">No. butaca</label>
                <input type="text" name="seat" id="seat">
            </div>
        </div>
    </div>
    `
}