% rebase('base.tpl')

<h1>Latest content</h1>

% if not content:
<p>No content</p>
% else:
    <ul>
        % for c in content:
        <li>
        {{ c.title }}
        </li>
        % end
    </ul>
% end
