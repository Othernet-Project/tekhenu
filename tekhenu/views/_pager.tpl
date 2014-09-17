<nav class="pager">
    % if c.pages > 1:
        % if c.page > 1:
        %# Translators, appears in pager
        <a class="page first" href="{{ i18n_path(h.add_qparam('p', str(1))) }}">{{ _('first') }}</a>
        %# Translators, appears in pager
        <a class="page prev" href="{{ i18n_path(h.add_qparam('p', str(c.page - 1))) }}">{{ _('previous') }}</a>
        % end

        % if c.page > 4:
        <span class="indicator">1 ...</span>
        % end

        % if c.page > 2:
        <a class="page link" href="{{ i18n_path(h.add_qparam('p', str(c.page - 2))) }}">{{ c.page - 2 }}</a>
        % end

        % if c.page > 1:
        <a class="page link" href="{{ i18n_path(h.add_qparam('p', str(c.page - 1))) }}">{{ c.page - 1 }}</a>
        % end

        <span class="page current">{{ c.page }}</span>

        % if c.page < c.pages:
        <a class="page link" href="{{ i18n_path(h.add_qparam('p', str(c.page + 1))) }}">{{ c.page + 1 }}</a>
        % end

        % if c.page < c.pages - 1:
        <a class="page link" href="{{ i18n_path(h.add_qparam('p', str(c.page + 2))) }}">{{ c.page + 2 }}</a>
        % end

        % if c.page < c.pages - 3:
        <span class="indicator">... {{ c.pages }}</span>
        % end

        % if c.page < c.pages:
        %# Translators, appears in pager
        <a class="page next" href="{{ i18n_path(h.add_qparam('p', str(c.page + 1))) }}">{{ _('next') }}</a>
        %# Translators, appears in pager
        <a class="page last" href="{{ i18n_path(h.add_qparam('p', str(c.pages))) }}">{{ _('last') }}</a>
        % end
    % end
</nav>
