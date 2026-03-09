        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-bordered">
                    <thead class="table-light">
                        <tr>
                            <td scope="row" colspan="2">
                                <strong>Competition name: </strong>
                                {{ competition.name|upper }}
                            </td>
                        </tr>
                        <tr>
                            <th scope="col"> Field </th>
                            <th scope="col"> Value </th>
                        </tr>
                    </thead>
                    <tr>
                        <td><strong> ID </strong></td>
                        <td> {{ competition.id }} </td>
                    </tr>
                </table>
            </div>
        </div>
