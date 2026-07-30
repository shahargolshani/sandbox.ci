# Copyright: (c) 2026, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

# Stub module utils for sandbox.ci.
# Changing any file in this directory triggers a full integration test run
# across ALL targets — this is the behaviour being validated by the sandbox CI.

function Get-SandboxInfo {
    <#
    .SYNOPSIS
    Returns a minimal info hashtable for sandbox module use.
    #>
    return @{
        collection = "sandbox.ci"
        purpose    = "Integration target detection mechanism validation"
    }
}

Export-ModuleMember -Function Get-SandboxInfo
