% rebase('base')

<section class="main content-details">
    <div class="inner">
        %# Translators, appears as page title on content details page if source page has not title
        <h1>{{ content.title or _('No title') }} <span class="status-{{ content.status }}">{{ content.status_title }}</span></h1>
        <p><a class="external" href="{{ content.url }}" target="_blank">{{ h.trunc(content.url, 40) }}</a></p>
        %# Translators, appears as label next to number of votes, should not be considered as a sentence
        <p>{{ content.votes }} <span>{{ ngettext('vote', 'votes', content.votes) }}</span></p>
        % if request.params.get('edit') == '1' and content.is_editable:
        <form class="content-edit" method="POST">
            {{! csrf_token }}
            <p>
            %# Translators, used as label for content title
            <label for="title">{{ _('title:') }}</label>
            {{! h.vinput('title', vals, _type="text") }}
            {{! h.field_error('title', errors) }}
            </p>
            <p>
            %# Translators, used as label for content title
            <label for="license">{{ _('license:') }}</label>
            {{! h.vselect('license', Content.LICENSES, vals) }}
            {{! h.field_error('license', errors) }}
            </p>
            <p class="buttons">
            <button type="submit">Save</button>
        </form>
        % else:
        <p>
        %# Translators, used as label for content title
        <span class="label">{{ _('title:') }}</span>
        {{ content.title or _('no title') }}
        % if content.is_editable:
            % include('_fix_button')
        % end
        </p>
        <p>
        %# Translators, used as label for content license
        <span class="label">{{ _('license:') }}</span>
        %# Translators, used instad of license name when license information is missing 
        {{ h.yesno(content.license, content.license_title, _('unknown')) }}
        % if content.is_editable:
            % include('_fix_button')
        % end
        </p>
        % end

        <h2>{{ _('Activity log') }}</h2>

        <ul class="log">
        % for entry in content.log:
            <li>
            <span class="timestamp">[{{ entry.timestamp }} UTC - {{ entry.ip_addr }}]</span>
            <span class="entry">{{ entry.title }}</span>
            </li>
        % end
        </ul>
    </div>
</section>

<aside class="suggestion-form">
    <div class="inner">
        % include('_suggestion_form')
    </div>
</aside>
