% rebase('base')

<section class="main">
    <div class="inner">
        %# Translators, section title above content listing
        <h1>{{ _('Latest content') }}</h1>

        <form>
            <p class="search">
            {{! h.vinput('q', vals, _type="text", _placeholder=_('Search')) }}
            <button type="submit">{{ _('Go') }}</button>
            </p>
            <p class="filters">
            {{! h.vselect('status', Content.STATI, vals, empty=_('Status')) }}
            {{! h.vselect('license', Content.LICENSES_SIMPLE, vals, empty=_('License')) }}
            {{! h.vselect('votes', Content.VOTES, vals, empty=_('Votes')) }}
            <button type="submit">{{ _('Filter') }}</button>
            <a class="button" href="{{ i18n_path('/') }}">{{ _('Reset') }}</a>
            </p>
        </form>

        % if not content.count:
        <p>No content</p>
        % else:
        <table>
            <thead>
                <tr>
                    <th>{{ _('title') }}</th>
                    <th class="center">{{ _('votes') }}</th>
                    <th class="center">{{ _('license') }}</th>
                    <th class="center">{{ _('status') }}</th>
                </tr>
            </thead>
            <tbody>
                % for c in content.items:
                <tr>
                    <td>
                    %# Translators, appears next to URL in content list when there is no title
                    <a class="link" href="{{ i18n_path(c.path) }}">{{ h.yesno(c.title, c.title, '%s (%s)' % (c.url, _('no title'))) }}</a>
                    </td>
                    
                    <td class="center">
                    % if c.is_editable:
                    <form class="inline" action="{{ i18n_path(c.path + '/votes/') }}" method="POST">
                    {{! csrf_token }}
                    {{! h.HIDDEN('back', request.path) }}
                    <button class="vote-up" name="vote" value="up">{{ _('vote up') }}</button>
                    <span class="count">{{ c.votes }}</span>
                    <button class="vote-down" name="vote" value="down">{{ _('vote down') }}</button>
                    </form>
                    % else:
                    {{ c.votes }}
                    % end
                    </td>

                    <td class="center">
                    <span class="license-{{ c.license_type }}">{{ c.license }}</span>
                    </td>
                    
                    <td class="center">
                    <span class="status-{{ c.status }}">{{ c.status_title }}</span>
                    </td>
                </tr>
                % end
            </tbody>
        </table>
        % include('_pager', c=content)
        <div class="legend">
            <p><span class="license-free"></span> {{ _('can be customized to improve readability and reduce payload') }}</p>
            <p><span class="license-nonfree"></span> {{ _('cannot be customized') }}</p>
            <p><span class="license-sponsored"></span> {{ _('sponsored') }}</p>
            <p><span class="license-unknown"></span> {{ _('not known') }}</p>
        </div>
        % end
    </div>
</section>

<aside class="suggestion-form">
    <div class="inner">
        % include('_suggestion_form')
    </div>
</aside>
