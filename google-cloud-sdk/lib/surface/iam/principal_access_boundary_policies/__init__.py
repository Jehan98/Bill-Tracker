# -*- coding: utf-8 -*- #
# Copyright 2024 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# NOTE: This file is autogenerated and should not be edited by hand.
# AUTOGEN_CLI_VERSION: HEAD
"""Manage PrincipalAccessBoundaryPolicy instances."""

from googlecloudsdk.calliope import base
from surface.iam.principal_access_boundary_policies import _init_extensions as extensions


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
@base.Autogenerated
@base.Hidden
class PrincipalAccessBoundaryPoliciesAlpha(
    extensions.PrincipalAccessBoundaryPoliciesAlpha
):
  """Manage PrincipalAccessBoundaryPolicy instances."""


@base.ReleaseTracks(base.ReleaseTrack.BETA)
@base.Autogenerated
class PrincipalAccessBoundaryPoliciesBeta(
    extensions.PrincipalAccessBoundaryPoliciesBeta
):
  """Manage PrincipalAccessBoundaryPolicy instances."""


@base.ReleaseTracks(base.ReleaseTrack.GA)
@base.Autogenerated
@base.Hidden
class PrincipalAccessBoundaryPoliciesGa(
    extensions.PrincipalAccessBoundaryPoliciesGa
):
  """Manage PrincipalAccessBoundaryPolicy instances."""
