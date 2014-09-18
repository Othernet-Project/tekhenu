% rebase('base')

<h1>{{ _('Content') }}</h1>

<form method="POST">
    {{! csrf_token }}
    <p class="controls">
    <a href="{{ i18n_path(h.add_qparam('select', '1')) }}">select all</a>
    <a href="{{ i18n_path(h.add_qparam('select', '0')) }}">deselect all</a>
    </p>
    <table>
        <thead>
            <tr>
                <th></th>
                <th>{{ _('title') }}</th>
                <th>{{ _('votes') }}</th>
                <th>{{ _('license') }}</th>
                <th>{{ _('archive') }}</th>
            </tr>
        </thead>
        <tbody>
            % for c in content.items:
            <tr>
                <td>
                    {{! h.vcheckbox('selection', c.key.id(), vals, default=sel) }}
                </td>
                <td>{{ c.title or c.url }}</td>
                <td>{{ c.votes }} (+{{c.upvotes}}/-{{c.downvotes}})</td>
                <td>{{ c.license_title }}</td>
                <td>{{ c.archive_title }}</td>
            </tr>
            % end
        </tbody>
    </table>
    <p class="buttons">
    <button>Click me!</button>
    </p>
</form>

